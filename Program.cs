using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;

namespace MAClientGUI
{
    static class Program
    {
        /// <summary>
        /// 应用程序的主入口点。
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new frmConfig());
        }
    }
    struct pluginItem
    {
        public string file_name;
        public string file_ext;
        public string author;
        public string plugin_name;
        public string version;
        public string tip;
        public string hooks;
        public string extra_cmd;
    }
    public class CtrlAnimator
    {
        public int duration = 35;
        public int sleep = 3;
        public int max_step = 30;
        public int inc_amp = 1;
        private Form mainFrm;
        

        public CtrlAnimator(Form mainFrm)
        {
            this.mainFrm = mainFrm;
        }
        public void ChangeHeight(Control ctl, int toheight)
        {
            Thread athread = new Thread(new ThreadStart(() =>
            {
                int done=0,ori=ctl.Height;
                int accel_time = Convert.ToInt32(duration/sleep*0.2);
                while(done<=duration/sleep && ((ori<toheight &&ctl.Height<toheight)||(ori>toheight &&ctl.Height>toheight))){
                    this.mainFrm.Invoke((MethodInvoker)(() =>
                    {
                        ctl.Height += (toheight-ori)*sleep/duration+Math.Sign(toheight-ori)*3;
                    }));
                    done += 1;
                    Thread.Sleep(sleep);
                }
            }));
            athread.Start();
        }
        public void ChangeOffsetY(Control ctl, int tooffset)
        {
            ctl.Location = new System.Drawing.Point(ctl.Location.X,ctl.Location.Y+tooffset);
        }
    }
    public class configParser
    {
        public string inipath;
        [DllImport("kernel32")]
        private static extern long WritePrivateProfileString(string section, string key, string val, string filePath);
        [DllImport("kernel32")]
        private static extern int GetPrivateProfileString(string section, string key, string def, StringBuilder retVal, int size, string filePath);
        [DllImport("Kernel32.dll")]
        static extern int WideCharToMultiByte(
          uint CodePage,
          uint dwFlags,
          [In, MarshalAs(UnmanagedType.LPWStr)]string lpWideCharStr,
          int cchWideChar,
          [Out, MarshalAs(UnmanagedType.LPStr)]StringBuilder lpMultiByteStr,
          int cbMultiByte,
          IntPtr lpDefaultChar, // Defined as IntPtr because in most cases is better to pass
          IntPtr lpUsedDefaultChar // NULL
          );
        private int buf_size=512;
        public configParser(string INIPath)
        {
            if (INIPath.IndexOf(":") == -1)
            {
                inipath = System.Environment.CurrentDirectory + "\\" + INIPath;
            }else
                inipath = INIPath;
        }

        public void Write(string Section, string Key, int Value)
        {
            this.Write(Section, Key, Value.ToString());
        }

        public void Write(string Section, string Key, bool Value)
        {
            this.Write(Section, Key, Value?"1":"0");
        }

        public void Write(string Section, string Key, decimal Value)
        {
            this.Write(Section, Key, Value.ToString());
        }

        public void Write(string Section, string Key, string Value)
        {
            /*if (Value.StartsWith("\"") && Value.EndsWith("\""))
                Value = "'" + Value + "'";
            else if (Value.StartsWith("'") && Value.EndsWith("'"))
                Value = "\"" + Value + "\"";*/
            WritePrivateProfileString(Section, Key, Value, this.inipath);
        }

        public string Read(string Section, string Key)
        {
            StringBuilder temp ;
            int i=0;
            int fac=0;
            do
            {
                fac++;
                temp = new StringBuilder(buf_size * fac);
                i = GetPrivateProfileString(Section, Key, "", temp, buf_size * fac, this.inipath);
                //MessageBox.Show(Key+i.ToString());
            } while (i == buf_size * fac - 1 || i == buf_size * fac - 2);
            return temp.ToString();
        }


        public int ReadInt(string Section, string Key)
        {
            string v = this.Read(Section, Key);
            if (v == "") v = "0";
            return int.Parse(v);
        }
        public float ReadFloat(string Section, string Key)
        {
            string v = this.Read(Section, Key);
            if (v == "") v = "0";
            return float.Parse(v);
        }
        public bool ReadBool(string Section, string Key)
        {
            string v = this.Read(Section, Key);
            return v=="1";
        }
        public bool ExistINIFile()
        {
            return File.Exists(inipath);
        }

        public List<string> EnumIniKey(string sectionName)
        {
            string[] IniText = File.ReadAllLines(inipath, Encoding.Default);
            List<string> KeyList = new List<string>();

            string curs = null;

            for (int i = 0; i != IniText.Length; i++)
            {
                string Text = IniText[i].Trim();
                if (Text == "")
                    continue;
                if (Text[0] == '[' && Text[Text.Length - 1] == ']')
                {
                    curs = Text;

                }
                else
                {

                    if (curs == "[" + sectionName + "]")
                        KeyList.Add(Text);
                }


            }
            return KeyList;

        }


    }


    public class  WndHdl
    { 
        [DllImport( "User32.dll ")] 
        public static extern System. IntPtr FindWindowEx(System. IntPtr parent, System. IntPtr childe, string strclass, string strname);
        private delegate bool WNDENUMPROC(IntPtr hWnd, int lParam);
        [DllImport("User32.dll ")] 
        private static extern bool EnumWindows(WNDENUMPROC lpEnumFunc, int lParam);
        //[DllImport("user32.dll")]
        //private static extern IntPtr FindWindowW(string lpClassName, string lpWindowName);
        [DllImport("User32.dll ")] 
        public static extern int GetWindowTextW(IntPtr hWnd, [MarshalAs(UnmanagedType.LPWStr)]StringBuilder lpString, int nMaxCount);
        [DllImport("User32.dll ")] 
        private static extern int GetClassNameW(IntPtr hWnd, [MarshalAs(UnmanagedType.LPWStr)]StringBuilder lpString, int nMaxCount);
        [DllImport("User32.dll ")] 
        private static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
        [DllImport("User32.dll ")] 
        private static extern bool IsWindowVisible(IntPtr hWnd);
        private const int SW_HIDE = 0;                                                          //常量，隐藏
        private const int SW_SHOWNORMAL = 1;                                                    //常量，显示，标准状态
        private const int SW_SHOWMINIMIZED = 2;                                                 //常量，显示，最小化
        private const int SW_SHOWMAXIMIZED = 3;                                                 //常量，显示，最大化
        private const int SW_SHOWNOACTIVATE = 4;                                                //常量，显示，不激活
        private const int SW_RESTORE = 9;                                                       //常量，显示，回复原状
        private const int SW_SHOWDEFAULT = 10;                                                  //常量，显示，默认
        
        [DllImport("user32")]
        public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int processId);
        public delegate void WinEventDelegate(IntPtr hWinEventHook, uint eventType,
            IntPtr hwnd, int idObject, int idChild, uint dwEventThread, uint dwmsEventTime);

        [DllImport("user32.dll")]
        public static extern IntPtr SetWinEventHook(uint eventMin, uint eventMax, IntPtr
           hmodWinEventProc, WinEventDelegate lpfnWinEventProc, uint idProcess,
           uint idThread, uint dwFlags);

        [DllImport("user32.dll")]
        public static extern bool UnhookWinEvent(IntPtr hWinEventHook);

        [DllImport("User32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);

        public struct WndInfo
        {
            public IntPtr hwnd;
            public string title;
            public int procid;
            public int threadid;
        }
        public static void hideWnd(WndInfo[] wnds)
        {
            foreach (WndInfo w in wnds)
            {
                ShowWindowAsync(w.hwnd, SW_HIDE);
            }
        }

        public static void hideWnd(WndInfo wnd)
        {
            WndInfo[] wnds = { wnd };
            hideWnd(wnds);
        }

        public static void showWnd(WndInfo[] wnds)
        {
            foreach (WndInfo w in wnds)
            {
                ShowWindowAsync(w.hwnd, SW_RESTORE);
            }
        }

        public static void showWndIfHided(WndInfo[] wnds)
        {
            foreach (WndInfo w in wnds)
            {
                if(!isVisible(w.hwnd))
                    ShowWindowAsync(w.hwnd, SW_RESTORE);
            }
        }

        public static WndInfo refreshTitle(WndInfo wnd)
        {
            StringBuilder sb = new StringBuilder(256);
            GetWindowTextW(wnd.hwnd, sb, sb.Capacity);
            wnd.title = sb.ToString();
            return wnd;
        }

        public static void showWnd(WndInfo wnd)
        {
            WndInfo[] wnds = { wnd };
            showWnd(wnds);
        }

        public static bool isVisible(IntPtr hwnd)
        {
            return IsWindowVisible(hwnd);
        }

        public static WndInfo[] findHwndbyTitleReg(String textReg) 
        {
            Regex rx = new Regex(textReg, RegexOptions.Compiled);
            List<WndInfo> wndList = new List<WndInfo>();

            //enum all desktop windows
            EnumWindows(delegate(IntPtr hWnd, int lParam)
            {
                StringBuilder sb = new StringBuilder(256);
                WndInfo w = new WndInfo();
                GetWindowTextW(hWnd, sb, sb.Capacity);
                if (rx.IsMatch(sb.ToString()))
                {
                    w.hwnd = hWnd;
                    w.title = sb.ToString();
                    w.threadid = GetWindowThreadProcessId(hWnd, out w.procid);
                    wndList.Add(w);
                }
                return true;
            }, 0);

            return wndList.ToArray();

        }
        public static WndInfo[] findHwndbyTitle(String text)
        {
            return findHwndbyTitleReg(text);
        }

        public static void showMe()
        {
        }

        public static void hideMe()
        {
        }

    }
    public class thook
    {
        const uint EVENT_OBJECT_NAMECHANGE = 0x800C;
        const uint WINEVENT_OUTOFCONTEXT = 0;
        public WndHdl.WndInfo r;
        public WndHdl.WinEventDelegate w;
        WndHdl.WinEventDelegate procDelegate;
        public bool exiting = false;
        [DllImport("user32")]
        public static extern
            bool GetMessage(ref Message lpMsg, IntPtr handle, uint mMsgFilterInMain, uint mMsgFilterMax);

        public thook(WndHdl.WndInfo f, WndHdl.WinEventDelegate e) 
        {
            r = f;
            MessageBox.Show(r.threadid.ToString()+";"+r.procid.ToString());
            w = e;
            procDelegate = new WndHdl.WinEventDelegate(w);
        }

        public thook(WndHdl.WinEventDelegate e)
        {
            w = e;
            procDelegate = new WndHdl.WinEventDelegate(w); 
        }

        public void threading_hook()
        {
            IntPtr hhook = WndHdl.SetWinEventHook(EVENT_OBJECT_NAMECHANGE, EVENT_OBJECT_NAMECHANGE, IntPtr.Zero,
                procDelegate, 0, 0, WINEVENT_OUTOFCONTEXT);
            Message msg = new Message();
            while (GetMessage(ref msg, IntPtr.Zero, 0, 0))
            {
                //stay here :)
                if (exiting)
                {
                    WndHdl.UnhookWinEvent(hhook);
                    break;
                }
            }
           
        }
    }
}

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
namespace MAClientGUI
{
    
    public partial class frmNiceTerm : Form
    {
        public frmNiceTerm()
        {
            InitializeComponent();
            this.outputWorker.WorkerReportsProgress = true;
            this.outputWorker.WorkerSupportsCancellation = true;
            this.outputWorker.DoWork += new DoWorkEventHandler(this.outputWorker_DoWork);
            this.outputWorker.ProgressChanged += new ProgressChangedEventHandler(this.outputWorker_ProgressChanged);
        }
        public Process process;
        public BackgroundWorker outputWorker = new BackgroundWorker();
        public Action kill_callback; 
        TextReader sr;
        public void StartProcess(string exec, string arg)
        {
            process = new Process();
            process.StartInfo.FileName = exec;
            process.StartInfo.Arguments = arg;
            //process.StartInfo.Arguments = "Z:/test.py";
            //process.StartInfo.FileName = "Z:/MAClient1.68/maclient_cli.exe";
            //process.StartInfo.Arguments = "Z:/MAClient1.68/config.ini t:e";
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardInput = true;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.EnvironmentVariables["NICE_TERM"] = "1";
            process.StartInfo.StandardOutputEncoding = Encoding.UTF8;
            process.StartInfo.CreateNoWindow = true;
            process.Start();
            sr = TextReader.Synchronized(this.process.StandardOutput);
            this.outputWorker.RunWorkerAsync();
        }

        private void outputWorker_DoWork(object sender, DoWorkEventArgs e)
        {
            while (!this.outputWorker.CancellationPending)
            {
                
                String line=null;
                while ((line = sr.ReadLine()) != null)
                {
                    this.outputWorker.ReportProgress(0, line+"\n");
                };
                /*do
                int buf = 0;
                StringBuilder builder = new StringBuilder();
                {
                    buf = this.sr.Read();
                    builder.Append((char)buf);
                    if ((char)buf == '\n') break;
                }
                while (buf > 0);*/
                Thread.Sleep(200);
            }
        }

        private void outputWorker_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            if (e.UserState is string)
            {
                string line = e.UserState as string;
                if (line.StartsWith("[SET-TITLE]")){
                    this.Text=line.Substring(11)+" - NiceTerm";
                    return;
                }
                //line = Encoding.GetEncoding(65001).GetString(Encoding.Default.GetBytes(line));
                int ori = richTextBox1.Text.Length;
                richTextBox1.AppendText(line);
                richTextBox1.ScrollToCaret();
                int length = line.Length;
                richTextBox1.Select(ori, length);
                if (line.StartsWith("DEBUG"))
                    richTextBox1.SelectionColor = Color.Green;
                else if (line.StartsWith("SLEEP"))
                    richTextBox1.SelectionColor = Color.Gray;
                else if (line.StartsWith("WARNING"))
                    richTextBox1.SelectionColor = Color.Yellow;
                else if (line.StartsWith("ERROR"))
                    richTextBox1.SelectionColor = Color.Red;
                else
                    richTextBox1.SelectionColor = richTextBox1.ForeColor;

            }
        }

        private void mnuExit_Click(object sender, EventArgs e)
        {
            if (process != null && !process.HasExited)
            {
                process.Kill();
                this.outputWorker.CancelAsync();
                this.Close();
                kill_callback();
            }
        }

        private void mnuTerminate_Click(object sender, EventArgs e)
        {
            MessageBox.Show(Encoding.GetEncoding(65001).GetString(Encoding.Default.GetBytes("服务(kr)1,거인 사이보그,14352")));
            /*IntPtr handle = process.Handle;
            IntPtr CTRL_KEY = new IntPtr(0x11);
            uint KEY_DOWN = 0x0100;
            uint KEY_UP = 0x0101;
            IntPtr C_KEY = new IntPtr(0x43);

            PostMessage(handle, KEY_DOWN, CTRL_KEY, IntPtr.Zero);
            PostMessage(handle, KEY_DOWN, C_KEY, IntPtr.Zero);
            PostMessage(handle, KEY_UP, C_KEY, IntPtr.Zero);
            PostMessage(handle, KEY_UP, CTRL_KEY, IntPtr.Zero);*/
        }


        private void frmNiceTerm_FormClosing(object sender, FormClosingEventArgs e)
        {
            mnuExit_Click(sender, e);
        }

        private void mnuAbout_Click(object sender, EventArgs e)
        {
            MessageBox.Show("NiceTerm是一个简单的终端模拟器，作为MAClientGUI的一部分开源。\n"+
            "https://github.com/fffonion/MAClient/tree/gui\n"+
            "图标来自Windows8的imageres.dll"
                ,"哈哈",MessageBoxButtons.OK,MessageBoxIcon.Information);
        }

        private void mnuSetFont_Click(object sender, EventArgs e)
        {
            FontDialog fontDialog = new FontDialog();
            fontDialog.Color = richTextBox1.ForeColor;
            fontDialog.AllowScriptChange = true;
            fontDialog.ShowColor = true;
            if (fontDialog.ShowDialog() != DialogResult.Cancel)
            {
                richTextBox1.Font = fontDialog.Font;
                richTextBox1.ForeColor = fontDialog.Color;
            }

        }
    }
}

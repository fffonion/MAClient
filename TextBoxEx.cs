using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Drawing;
using System.Runtime.InteropServices;

namespace MAClientGUI
{
   
    public partial class TextBoxEx : System.Windows.Forms.TextBox
    {

        [DllImport("user32.dll")]
        static extern IntPtr GetWindowDC(IntPtr hWnd);
        [DllImport("user32.dll")]
        static extern bool ReleaseDC(IntPtr hWnd, IntPtr hDC);

        public TextBoxEx()
            : base()
        {
            this.BorderStyle = BorderStyle.FixedSingle;
            this.UpdateStyles();
            BgInfo b;
            b.percent = 1;
            b.color = Color.FromArgb(128, 128, 0, 0);
            this.Tag = b;
        }
        public struct BgInfo
        {
            public float percent;
            public Color color;
        }

        public void setColor(Color c)
        {
            BgInfo b=(BgInfo)this.Tag;
            b.color = c;
            this.Tag = b;
            this.Invalidate();
        }

        public void setPercent(float p)
        {
            BgInfo b = (BgInfo)this.Tag;
            b.percent = p;
            this.Tag = b;
            this.Invalidate();
        }

        protected override void WndProc(ref Message m)
        {
            base.WndProc(ref m);
            if (m.Msg == 0xf || m.Msg == 0x133)
            {
                DrawBG();
            }
        }

        public void DrawBG() {
            float w = ((BgInfo)this.Tag).percent;
            Color c = ((BgInfo)this.Tag).color;
            DrawBG(w,c);
        }

        public void DrawBG(float percent, Color objcolor)
        {
            /*try
            {
                if (long.Parse(this.Text) % 2 == 0) objcolor = System.Drawing.Color.Blue;
                else objcolor = System.Drawing.Color.Red;
            }
            catch (FormatException) {}*/
            //System.Drawing.Pen pen = pen = new Pen(objcolor, 30);
            IntPtr hDC = GetWindowDC(this.Handle);
            if (hDC.ToInt32() == 0)
            {
                return;
            }
            System.Drawing.Graphics g = Graphics.FromHdc(hDC);
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            Brush brush = new SolidBrush(objcolor);
            g.FillRectangle(brush, 0, 0, this.Width*percent, this.Height);
            //g.DrawRectangle(pen, 0, 0, control.Width - Nwidth, control.Height - Nwidth);
            brush.Dispose();
            ReleaseDC(this.Handle, hDC);
        }

        /*protected override void OnGotFocus(EventArgs e)
        {
            base.OnGotFocus(e);
            //BackColor = Color.MistyRose;
            //Tag = System.Drawing.Color.Red;
        }*/

        /*protected override void OnTextChanged(EventArgs e)
        {
            base.OnTextChanged(e);
            if (this.Text.Length>0)
            setColor(Color.FromArgb(128, int.Parse(this.Text), 255, 255));
            this.Invalidate();
        }*/
    }
}

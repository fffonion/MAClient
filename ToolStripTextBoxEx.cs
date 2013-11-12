using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace maClientGUI
{
    public partial class ToolStripTextBoxEx : ToolStripControlHost
    {
        private void init()
        {
            this.Enabled = false;
            this.AutoSize = false;
            //this.Dock = DockStyle.Fill;
            //this.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            this.Width = 175;
            this.Height = 50;
            this.RightToLeft = RightToLeft.Yes;
        }

        public ToolStripTextBoxEx() : base(new TextBoxEx()) 
        {
            init();
        }

        public ToolStripTextBoxEx(Color color) : base(new TextBoxEx()) 
        {
            init();
            this.setColor(color);
        }

        public TextBoxEx TextBoxExCtl
        {
            get
            {
                return base.Control as TextBoxEx;
            }
        }

        public void setColor(Color c)
        {
            TextBoxExCtl.setColor(c);
            TextBoxExCtl.Invalidate();
        }

        public void setPercent(float p)
        {
            TextBoxExCtl.setPercent(p);
            TextBoxExCtl.Invalidate();
        }

    }
}

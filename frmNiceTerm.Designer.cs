namespace MAClientGUI
{
    partial class frmNiceTerm
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmNiceTerm));
            this.richTextBox1 = new System.Windows.Forms.RichTextBox();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.mnuCtrl = new System.Windows.Forms.ToolStripMenuItem();
            this.mnuTerminate = new System.Windows.Forms.ToolStripMenuItem();
            this.mnuExit = new System.Windows.Forms.ToolStripMenuItem();
            this.mnuSetup = new System.Windows.Forms.ToolStripMenuItem();
            this.mnuSetFont = new System.Windows.Forms.ToolStripMenuItem();
            this.mnuAbout = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // richTextBox1
            // 
            this.richTextBox1.BackColor = System.Drawing.SystemColors.InactiveCaptionText;
            this.richTextBox1.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.richTextBox1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.richTextBox1.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.richTextBox1.ForeColor = System.Drawing.SystemColors.Menu;
            this.richTextBox1.Location = new System.Drawing.Point(0, 28);
            this.richTextBox1.Name = "richTextBox1";
            this.richTextBox1.ReadOnly = true;
            this.richTextBox1.ScrollBars = System.Windows.Forms.RichTextBoxScrollBars.Vertical;
            this.richTextBox1.Size = new System.Drawing.Size(793, 490);
            this.richTextBox1.TabIndex = 2;
            this.richTextBox1.Text = "";
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.mnuCtrl,
            this.mnuSetup,
            this.mnuAbout});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(793, 28);
            this.menuStrip1.TabIndex = 3;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // mnuCtrl
            // 
            this.mnuCtrl.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.mnuTerminate,
            this.mnuExit});
            this.mnuCtrl.Name = "mnuCtrl";
            this.mnuCtrl.Size = new System.Drawing.Size(69, 24);
            this.mnuCtrl.Text = "控制(&F)";
            // 
            // mnuTerminate
            // 
            this.mnuTerminate.Enabled = false;
            this.mnuTerminate.Name = "mnuTerminate";
            this.mnuTerminate.Size = new System.Drawing.Size(127, 24);
            this.mnuTerminate.Text = "中断(&T)";
            this.mnuTerminate.Click += new System.EventHandler(this.mnuTerminate_Click);
            // 
            // mnuExit
            // 
            this.mnuExit.Name = "mnuExit";
            this.mnuExit.Size = new System.Drawing.Size(127, 24);
            this.mnuExit.Text = "退出(&E)";
            this.mnuExit.Click += new System.EventHandler(this.mnuExit_Click);
            // 
            // mnuSetup
            // 
            this.mnuSetup.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.mnuSetFont});
            this.mnuSetup.Name = "mnuSetup";
            this.mnuSetup.Size = new System.Drawing.Size(71, 24);
            this.mnuSetup.Text = "设置(&C)";
            // 
            // mnuSetFont
            // 
            this.mnuSetFont.Name = "mnuSetFont";
            this.mnuSetFont.Size = new System.Drawing.Size(126, 24);
            this.mnuSetFont.Text = "字体(&F)";
            this.mnuSetFont.Click += new System.EventHandler(this.mnuSetFont_Click);
            // 
            // mnuAbout
            // 
            this.mnuAbout.Name = "mnuAbout";
            this.mnuAbout.Size = new System.Drawing.Size(72, 24);
            this.mnuAbout.Text = "关于(&A)";
            this.mnuAbout.Click += new System.EventHandler(this.mnuAbout_Click);
            // 
            // frmNiceTerm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(793, 518);
            this.Controls.Add(this.richTextBox1);
            this.Controls.Add(this.menuStrip1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "frmNiceTerm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "NiceTerm";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.frmNiceTerm_FormClosing);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.RichTextBox richTextBox1;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem mnuCtrl;
        private System.Windows.Forms.ToolStripMenuItem mnuAbout;
        private System.Windows.Forms.ToolStripMenuItem mnuTerminate;
        private System.Windows.Forms.ToolStripMenuItem mnuExit;
        private System.Windows.Forms.ToolStripMenuItem mnuSetup;
        private System.Windows.Forms.ToolStripMenuItem mnuSetFont;
    }
}


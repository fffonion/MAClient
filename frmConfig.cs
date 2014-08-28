using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using System.IO;
using System.Text.RegularExpressions;
using System.Runtime.InteropServices;
using System.Diagnostics;

namespace MAClientGUI
{
    public partial class frmConfig : Form
    {
        configParser cf;
        string server;
        string maclient_path;
        List<frmNiceTerm> niceterms = new List<frmNiceTerm>();
        public frmConfig()
        {
            InitializeComponent();
            maclient_path = System.Environment.CurrentDirectory + "\\maclient_cli.exe";
            
        }

        private void btnChooseCfg_Click(object sender, EventArgs e)
        {
            //if (cboCfgFile.Items.Count == 0)
            //{
            //if (MessageBox.Show("木有发现配置文件，是否手动寻找？", "呵呵", MessageBoxButtons.YesNo, MessageBoxIcon.Error) == DialogResult.No)
            //    return;

            OpenFileDialog fileDialog1 = new OpenFileDialog();
            fileDialog1.Filter = "配置文件(*.ini)|*.ini|所有文件(*.*)|*.*";
            fileDialog1.FilterIndex = 1;
            fileDialog1.RestoreDirectory = true;
            if (fileDialog1.ShowDialog() == DialogResult.OK)
            {
                if (cboCfgFile.FindStringExact(fileDialog1.FileName) == -1)
                {
                    if (fileDialog1.FileName.IndexOf(":") == -1)
                        cboCfgFile.Items.Add(System.Environment.CurrentDirectory + "\\" + fileDialog1.FileName);
                    else
                        cboCfgFile.Items.Add(fileDialog1.FileName);
                    cboCfgFile.SelectedIndex = cboCfgFile.FindStringExact(fileDialog1.FileName);
                }
            }
            else
                return;
            //}
            cf = new configParser(cboCfgFile.Text);
            tabControl1.Enabled = true;
            refreshAll();
            refreshCond();

        }

        private void refreshAccount()
        {
            lblUsername.Text = cf.Read("account_" + server, "username");
            lblPswd.Tag = cf.Read("account_" + server, "password");
        }
        private void refreshAll()
        {
            server = cf.Read("system", "server");
            switch (server)
            {
                case "cn":
                    cboServer.SelectedIndex = 0;
                    break;
                case "cn2":
                    cboServer.SelectedIndex = 1;
                    break;
                case "cn3":
                    cboServer.SelectedIndex = 2;
                    break;
                case "tw":
                    cboServer.SelectedIndex = 3;
                    break;
                case "kr":
                    cboServer.SelectedIndex = 4;
                    break;
                case "jp":
                    cboServer.SelectedIndex = 5;
                    break;
                case "sg":
                    cboServer.SelectedIndex = 6;
                    break;
            }
            refreshAccount();
            cboLogLevel.SelectedIndex = cf.ReadInt("system", "loglevel");
            //txtTaskName.Text = cf.Read("system", "taskname");
            cbTask.Items.Clear();
            List<string> tsl = cf.EnumIniKey("tasker");

            foreach (string ts in tsl)
            {
                cbTask.Items.Add(ts.Split('=')[0].Trim());

            }
            cbTask.Items.Add("新建");
            if (cbTask.Items.Count > 0)
            {

                int idx = cbTask.Items.IndexOf(cf.Read("system", "taskname"));
                if (idx == -1)
                    idx = 0;
                cbTask.SelectedIndex = idx;
            }
            else
            {
                cbTask.SelectedIndex = 0;
            }
            cboDeckList.Items.Clear();
            cboSetCard.Items.Clear();
            cboSetCard.Items.Add("选择…");
            List<string> lst2 = cf.EnumIniKey("carddeck");
            foreach (string ts in lst2)
            {
                cboDeckList.Items.Add(ts.Split('=')[0].Trim());
                cboSetCard.Items.Add(ts.Split('=')[0].Trim());
            }
            cboSetCard.SelectedIndex = 0;
            numTaskTimes.Value = cf.ReadInt("system", "tasker_times");
            numFactorTimes.Value = cf.ReadInt("system", "try_factor_times");
            numFactorSleep.Value = cf.ReadInt("system", "factor_sleep");
            numExploreSleep.Value = cf.ReadInt("system", "explore_sleep");
            numFairyTimes.Value = cf.ReadInt("system", "fairy_battle_times");
            chkAutoUpdate.Checked = cf.ReadBool("system", "auto_update");
            chkUsePlugins.Checked = cf.ReadBool("system", "enable_plugin");
            chkAllowLongSleep.Checked = cf.ReadBool("system", "allow_long_sleep");
            txtReconnectGap.Text = cf.Read("system", "reconnect_gap");
            if (txtReconnectGap.Text == "")
            {
                txtReconnectGap.Text = "0";
                cboReconnectGapIndicator.SelectedIndex = 0;
            }
            else if (new Regex(@"\d+\:\d+", RegexOptions.Compiled).IsMatch(txtReconnectGap.Text))
                cboReconnectGapIndicator.SelectedIndex = 2;
            else if (txtReconnectGap.Text == "0")
                cboReconnectGapIndicator.SelectedIndex = 0;
            else
                cboReconnectGapIndicator.SelectedIndex = 1;
            numAutoRT.Value = (decimal)cf.ReadFloat("tactic", "auto_red_tea");
            numAutoGT.Value = (decimal)cf.ReadFloat("tactic", "auto_green_tea");
            cboAutoRTLv.SelectedIndex = cf.ReadInt("tactic", "auto_red_tea_level");
            numDelay.Value = (decimal)cf.ReadFloat("system", "delay");
            numInstantFight.Value = cf.ReadInt("tactic", "fairy_final_kill_hp");
            numAutoDelFriend.Value = cf.ReadInt("tactic", "del_friend_day");
            cboSellCardWarning.SelectedIndex = cf.ReadInt("tactic", "sell_card_warning");

            chkStirctBC.Checked = cf.ReadBool("tactic", "strict_bc");
            chkAutoChooseRT.Checked = cf.ReadBool("tactic", "auto_choose_red_tea");
            chkAutoGreet.Checked = cf.ReadBool("tactic", "auto_greet");
            chkAutoExplore.Checked = cf.ReadBool("tactic", "auto_explore");
            chkAutoSellCard.Checked = cf.ReadBool("tactic", "auto_sell_card");
            chkAutoFPGacha.Checked = cf.ReadBool("tactic", "auto_fp_gacha");
            chkGachaBuild.Checked = cf.ReadBool("tactic", "auto_build");
            chkFairyRewards.Checked = cf.ReadBool("tactic", "auto_fairy_rewards");
            chkFPGachaBulk.Checked = cf.ReadBool("tactic", "fp_gacha_bulk");
            chkAni.Checked = cf.ReadBool("system", "display_ani");
            chkSaveTraffic.Checked = cf.ReadBool("system", "save_traffic");
            chkNewFactor.Checked = cf.ReadBool("tactic", "factor_getnew");
            txtFairySleep.Text = cf.Read("system", "fairy_battle_sleep");
            numFairySleepFactor.Value = (decimal)cf.ReadFloat("system", "fairy_battle_sleep_factor");
            txtGreetWords.Text = cf.Read("tactic", "greet_words");

            txtDisabledPlugins.Text = cf.Read("plugin", "disabled");
            //button10.Text = "开始任务" + txtTaskName.Text;
            setToolTipText();
            refreshOverride();
        }

        private void refreshOverride(){
            txtOverrideUA.Text = cf.Read("system", "user-agent");
            txtOverrideToken.Text = cf.Read("system", "device_token");
            txtOverrideVersion.Text = cf.Read("system", "app_ver_" + server.Substring(0, 2));
        }

        private void refreshCond()
        {
            //txtCondTasker.Text = cf.Read("tasker", txtTaskName.Text);
            txtCondTasker.Text = cf.Read("tasker", cbTask.Items[cbTask.SelectedIndex].ToString());
            txtCondFairy.Text = cf.Read("condition", "fairy_select");
            txtCondExplore.Text = cf.Read("condition", "explore_area");
            txtCondFloor.Text = cf.Read("condition", "explore_floor");
            txtCondCarddeck.Text = cf.Read("condition", "fairy_select_carddeck");
            //只有一个卡组名，则两边引号会被剥掉，加回去
            if (!txtCondCarddeck.Text.Contains("\"") && !txtCondCarddeck.Text.Contains("'"))
                txtCondCarddeck.Text = "'" + txtCondCarddeck.Text + "'";
            //同理
            if (!txtCondTasker.Text.Contains("\"") && !txtCondTasker.Text.Contains("'"))
                txtCondTasker.Text = "'" + txtCondTasker.Text + "'";
            txtCondFactor.Text = cf.Read("condition", "factor");
            txtCondSell.Text = cf.Read("condition", "select_card_to_sell");
        }

        private void saveAll()
        {
            cf.Write("account_" + server, "username", lblUsername.Text);
            cf.Write("account_" + server, "password", lblPswd.Tag.ToString());
            cf.Write("system", "server", server);
            cf.Write("system", "loglevel", cboLogLevel.SelectedIndex);
            //cf.Write("system", "taskname",txtTaskName.Text);
            cf.Write("system", "taskname", cbTask.Items[cbTask.SelectedIndex].ToString());
            cf.Write("system", "tasker_times", numTaskTimes.Value);
            cf.Write("system", "try_factor_times", numFactorTimes.Value);
            cf.Write("system", "factor_sleep", numFactorSleep.Value);
            cf.Write("system", "explore_sleep", numExploreSleep.Value);
            cf.Write("system", "fairy_battle_times", numFairyTimes.Value);
            cf.Write("tactic", "sell_card_warning", cboSellCardWarning.SelectedIndex);
            cf.Write("system", "auto_update", chkAutoUpdate.Checked);
            cf.Write("system", "enable_plugin", chkUsePlugins.Checked);
            cf.Write("system", "reconnect_gap", txtReconnectGap.Text);
            cf.Write("system", "allow_long_sleep", chkAllowLongSleep.Checked);

            cf.Write("tactic", "auto_green_tea", numAutoGT.Value);
            cf.Write("tactic", "auto_red_tea", numAutoRT.Value);
            cf.Write("tactic", "auto_red_tea_level", cboAutoRTLv.SelectedIndex);
            cf.Write("system", "delay", numDelay.Value);
            cf.Write("tactic", "fairy_final_kill_hp", numInstantFight.Value);
            cf.Write("tactic", "del_friend_day", numAutoDelFriend.Value);

            cf.Write("tactic", "strict_bc", chkStirctBC.Checked);
            cf.Write("tactic", "auto_greet", chkAutoGreet.Checked);
            cf.Write("tactic", "auto_explore", chkAutoExplore.Checked);
            cf.Write("tactic", "auto_sell_card", chkAutoSellCard.Checked);
            cf.Write("tactic", "auto_fp_gacha", chkAutoFPGacha.Checked);
            cf.Write("tactic", "auto_build", chkGachaBuild.Checked);
            cf.Write("tactic", "auto_fairy_rewards", chkFairyRewards.Checked);
            cf.Write("tactic", "fp_gacha_bulk", chkFPGachaBulk.Checked);
            cf.Write("tactic", "auto_choose_red_tea", chkAutoChooseRT.Checked);
            cf.Write("system", "display_ani", chkAni.Checked);
            cf.Write("system", "save_traffic", chkSaveTraffic.Checked);
            cf.Write("system", "fairy_battle_sleep", txtFairySleep.Text);
            cf.Write("system", "fairy_battle_sleep_factor", numFairySleepFactor.Value);
            cf.Write("tactic", "greet_words", txtGreetWords.Text);
            cf.Write("tactic", "factor_getnew", chkNewFactor.Checked);

            cf.Write("plugin", "disabled", txtDisabledPlugins.Text);

            saveOverride();
        }
        private void saveOverride()
        {
            if (txtOverrideUA.Text!="")
                cf.Write("system", "user-agent", txtOverrideUA.Text);
            if (txtOverrideToken.Text != "")
                cf.Write("system", "device_token", txtOverrideToken.Text);
            if (txtOverrideVersion.Text!="")
                cf.Write("system", "app_ver_" + server.Substring(0, 2), txtOverrideVersion.Text);
        }

        private void saveCond()
        {
            //cf.Write("tasker", txtTaskName.Text, txtCondTasker.Text);
            cf.Write("tasker", cbTask.Items[cbTask.SelectedIndex].ToString(), txtCondTasker.Text);
            cf.Write("condition", "fairy_select", txtCondFairy.Text);
            cf.Write("condition", "explore_area", txtCondExplore.Text);
            cf.Write("condition", "explore_floor ", txtCondFloor.Text);
            cf.Write("condition", "fairy_select_carddeck ", txtCondCarddeck.Text);
            cf.Write("condition", "factor ", txtCondFactor.Text);
            cf.Write("condition", "select_card_to_sell  ", txtCondSell.Text);
        }

        private void setToolTipText()
        {
            Func<decimal, string> loopTimeConv = l => { return (l == 0 ? "无限" : l.ToString()); };
            toolTip1.SetToolTip(this.cboLogLevel, "过滤输出到屏幕的信息");
            toolTip1.SetToolTip(this.numTaskTimes, "循环执行" + loopTimeConv(numTaskTimes.Value) + "次tasker任务");
            toolTip1.SetToolTip(this.numFactorTimes, "随机选择" + loopTimeConv(numFactorTimes.Value) + "次碎片进行因子战");
            toolTip1.SetToolTip(this.numFairyTimes, "循环刷新" + loopTimeConv(numFairyTimes.Value) + "次妖精列表以选择妖精");
            toolTip1.SetToolTip(this.chkStirctBC, "如果启用，当设定卡组cost小于当前BC时认为BC不足");
            toolTip1.SetToolTip(this.chkAutoSellCard, "如果启用，当卡片持有数>=可持有卡片数上限时时，按照条件设置中的计算值选择卡片贩卖");
            toolTip1.SetToolTip(this.chkAutoFPGacha, "如果启用，当基友点>=上限x0.9时，进行一次基友点转蛋");
            toolTip1.SetToolTip(this.chkFairyRewards, "仅限妖精战奖励，不含礼物盒内的奖励");
            toolTip1.SetToolTip(this.chkAni, "如果启用，将显示\"Connecting...\"动画");
            toolTip1.SetToolTip(this.chkSaveTraffic, "如果启用，当前使用舔刀卡组min时，将不下载战斗结果；当持有卡片数较多时效果显著");
            toolTip1.SetToolTip(this.txtFairySleep, "格式为 开始钟点,结束钟点,刷新间隔(分)，|分割");
            toolTip1.SetToolTip(this.chkFPGachaBulk, "如果不启用，每次绊转蛋只进行一回转蛋");
            toolTip1.SetToolTip(this.numInstantFight, "已进行一次战斗后，若妖精血量少于这个值，立即再进行一次战斗");
            toolTip1.SetToolTip(this.chkAutoUpdate, "如果开启，在服务器更新活动后，会自动下载新的卡牌数据和道具数据");
            toolTip1.SetToolTip(this.cboReservedName, "特殊卡组是为了实现某些逻辑，不是真正的卡组\n不打怪卡组需要MAClient1.67及以上版本");
            toolTip1.SetToolTip(this.chkAutoChooseRT, "开启后若拥有半红则优先使用\n当嗑半红不足以支持当前卡组cost时，自动嗑全红");
            toolTip1.SetToolTip(this.chkAllowLongSleep, "在某些操作系统上后台进程长时间睡眠会被kill，可以禁用此项");
        }
        private void frmConfig_Load(object sender, EventArgs e)
        {
            //setToolTipText();
            this.Text += (" v" + Application.ProductVersion + " (for MAClient v1.71+)");
            tabControl1.Enabled = false;
            DirectoryInfo folder = new DirectoryInfo(System.Environment.CurrentDirectory);
            foreach (FileInfo file in folder.GetFiles("*.ini"))
            {
                cboCfgFile.Items.Add(file);
            }
            if (cboCfgFile.Items.Count > 0)
                cboCfgFile.SelectedIndex = 0;
            Control.CheckForIllegalCrossThreadCalls = false;//丑就丑点吧www
            cboReservedName.SelectedIndex = 0;
            lblCodePage.Text = Encoding.Default.CodePage + "/" + Encoding.Default.EncodingName;
        }

        private void btnGoBack_Click(object sender, EventArgs e)
        {
            refreshAll();
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            saveAll();
        }

        private void cboServer_SelectedIndexChanged(object sender, EventArgs e)
        {
            string[] slist = { "cn", "cn2", "cn3", "tw", "kr", "jp","sg" };
            server = slist[cboServer.SelectedIndex];
            refreshAccount();
            refreshOverride();
            if (cboServer.SelectedIndex >= 4 && cboServer.SelectedIndex <6)
                chkUseNiceTerm.Checked = true;
            else
                chkUseNiceTerm.Checked = false;
        }

        private void cboCfgFile_SelectedIndexChanged(object sender, EventArgs e)
        {
            cf = new configParser(cboCfgFile.Text);
            tabControl1.Enabled = true;
            refreshAll();
            refreshCond();
            lblCfgEnc.Text = GetEncType(cboCfgFile.Text).EncodingName;
            if (lblCfgEnc.Text != "Unicode (UTF-8)" && !cf.ReadBool("MAClientGUI","no_enc_warning"))
                lblEncWarning.Visible = true;
            else lblEncWarning.Visible = false;
            lblEncWarningQuestion.Visible = lblEncWarning.Visible;
        }


        private void lblUsername_Click(object sender, EventArgs e)
        {
            txtUsername.Text = lblUsername.Text;
            txtUsername.Visible = true;
            txtUsername.Focus();
        }

        private void lblPswd_Click(object sender, EventArgs e)
        {
            txtPswd.Text = lblPswd.Tag.ToString();
            txtPswd.Visible = true;
            txtPswd.Focus();
        }

        private void txtUsername_Leave(object sender, EventArgs e)
        {
            lblUsername.Text = txtUsername.Text;
            txtUsername.Visible = false;
            cf.Write("account_" + server, "user_id", "");
        }

        private void txtPswd_Leave(object sender, EventArgs e)
        {
            lblPswd.Tag = txtPswd.Text;
            txtPswd.Visible = false;
        }

        private void checkBox9_CheckedChanged(object sender, EventArgs e)
        {
            txtPswd.PasswordChar = checkBox9.Checked ? '☺' : (char)0;
        }
        /// <summary>
        /// 任务选项卡！
        /// </summary>
        private void addTaskerCond(string cond)
        {
            if (lblTaskerCache.Text != "")
                lblTaskerCache.Text += " and ";
            lblTaskerCache.Text += cond;
        }
        private void addTaskerThen(string then)
        {
            if (!lblTaskerCache.Text.EndsWith(" or 'fyb'"))
                lblTaskerCache.Text += " and  or 'fyb'";
            else
            {
                lblTaskerCache.Text = lblTaskerCache.Text.Replace("' or 'fyb'", "| or 'fyb'");
                then = then.Remove(0, 1);
            }
            lblTaskerCache.Text = lblTaskerCache.Text.Replace(" or 'fyb'", then + " or 'fyb'");
        }
        private void btnTaskerBC_Click(object sender, EventArgs e)
        {

            addTaskerCond(textBox1.Text + "<=BC<=" + textBox2.Text);
            btnTaskerBC.Enabled = false;
        }

        private void btnTaskerAP_Click(object sender, EventArgs e)
        {
            addTaskerCond(textBox3.Text + "<=AP<=" + textBox4.Text);
            btnTaskerAP.Enabled = false;
        }
        private void button18_Click(object sender, EventArgs e)
        {
            addTaskerCond("FAIRY_ALIVE");
            button18.Enabled = false;
            button17.Enabled = false;
        }
        private void button53_Click(object sender, EventArgs e)
        {
            addTaskerCond("(" + numericUpDown5.Value.ToString() + "," + numericUpDown4.Value.ToString() + ")<(HH,MM)<(" +
                numericUpDown3.Value.ToString() + "," + numericUpDown2.Value.ToString() + ")");
            button53.Enabled = false;
        }
        private void button17_Click(object sender, EventArgs e)
        {
            addTaskerCond("not FAIRY_ALIVE");
            button18.Enabled = false;
            button17.Enabled = false;
        }
        private void button71_Click(object sender, EventArgs e)
        {
            addTaskerCond("GUILD_ALIVE");
            button71.Enabled = false;
            button70.Enabled = false;
        }
        private void button70_Click(object sender, EventArgs e)
        {
            addTaskerCond("not GUILD_ALIVE");
            button71.Enabled = false;
            button70.Enabled = false;
        }
        private void button52_Click(object sender, EventArgs e)
        {
            addTaskerThen("'fyb " + numericUpDown1.Value + "'");
        }
        private void btnTaskerSave_Click(object sender, EventArgs e)
        {
            if (txtCondTasker.Text == "")
                txtCondTasker.Text = "'fyb'";
            if (!lblTaskerCache.Text.EndsWith(" or 'fyb'"))
                lblTaskerCache.Text += " and 'fyb' or 'fyb'";
            txtCondTasker.Text = txtCondTasker.Text.Replace("or 'fyb'", "or ('fyb')");
            txtCondTasker.Text = txtCondTasker.Text.Replace("'fyb'", lblTaskerCache.Text);
            lblTaskerCache.Text = "";
            btnTaskerBC.Enabled = true;
            btnTaskerAP.Enabled = true;
            button17.Enabled = true;
            button18.Enabled = true;
            button70.Enabled = true;
            button71.Enabled = true;
            button53.Enabled = true;
        }

        private void btnDefault_Click(object sender, EventArgs e)
        {
            cboLogLevel.SelectedIndex = 2;
            numTaskTimes.Value = 50;
            numFactorTimes.Value = 20;
            numFactorSleep.Value = 10;
            numExploreSleep.Value = 2;
            numFairyTimes.Value = 20;
            cboSellCardWarning.SelectedIndex = 1;

            numAutoRT.Value = 0;
            numAutoGT.Value = 0;
            cboAutoRTLv.SelectedIndex = 1;
            numDelay.Value = 2;
            numInstantFight.Value = 30000;
            numAutoDelFriend.Value = 5;
            chkAutoUpdate.Checked = true;
            chkUsePlugins.Checked = true;
            chkAllowLongSleep.Checked = true;
            txtReconnectGap.Text = "5";
            
            chkStirctBC.Checked = true;
            chkAutoChooseRT.Checked = true;
            chkAutoGreet.Checked = true;
            chkAutoExplore.Checked = true;
            chkAutoSellCard.Checked = true;
            chkAutoFPGacha.Checked = true;
            chkGachaBuild.Checked = true;
            chkFairyRewards.Checked = true;
            chkFPGachaBulk.Checked = true;
            chkAni.Checked = true;
            chkSaveTraffic.Checked = false;
            chkNewFactor.Checked = true;
            chkAutoUpdate.Checked = true;
            txtFairySleep.Text = "0,4,6|4,7,4|7,8,2|8,11,2|11,14,1|14,16,2|16,19,0.8|19,21,1.5|21,24,2";
            numFairySleepFactor.Value = 1;
            txtGreetWords.Text = "你好！";

            //button10.Text = "开始任务" + txtTaskName.Text;
            setToolTipText();
        }

        private void btnTaskerReset_Click(object sender, EventArgs e)
        {
            lblTaskerCache.Text = "";
            btnTaskerBC.Enabled = true;
            btnTaskerAP.Enabled = true;
            button17.Enabled = true;
            button18.Enabled = true;
            button70.Enabled = true;
            button71.Enabled = true;
        }
        private void btnTaskerSetCard_Click(object sender, EventArgs e)
        {
            if(cboSetCard.SelectedIndex!=0)
                addTaskerThen("'sc " + cboSetCard.Text + "'");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            addTaskerThen("'e'");
        }

        private void button2_Click(object sender, EventArgs e)
        {
            string sel_lake = "";
            if (textBox28.Text != "")
                sel_lake = " lake:" + textBox28.Text;
            addTaskerThen("'fcb " + txtTaskerBCLimit.Text + sel_lake + "'");
        }
        private void button54_Click(object sender, EventArgs e)
        {
            addTaskerThen("'sleep " + numericUpDown6.Value.ToString() + "'");
        }
        /// <summary>
        /// 秘境选项卡！
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void addExploreCond(string cond)
        {
            if (!chkSuperPrefExplore.Checked)
                cond = cond.Replace("$.", "area.");
            if (txtCondExplore.Text != "" && !txtCondExplore.Text.TrimEnd().EndsWith("|"))
                txtCondExplore.Text += " and ";
            txtCondExplore.Text += cond;
        }

        private void button9_Click(object sender, EventArgs e)
        {
            addExploreCond("not FAIRY_ALIVE");
        }

        private void button7_Click(object sender, EventArgs e)
        {
            addExploreCond("$.NOT_FINNISHED");
        }

        private void button4_Click(object sender, EventArgs e)
        {
            addExploreCond("$.IS_EVENT");
        }
        private void button61_Click(object sender, EventArgs e)
        {
            addExploreCond("$.IS_GUILD");
        }
        private void button8_Click(object sender, EventArgs e)
        {
            addExploreCond("FAIRY_ALIVE");
        }
        private void button69_Click(object sender, EventArgs e)
        {
            addExploreCond("GUILD_ALIVE");
        }
        private void button68_Click(object sender, EventArgs e)
        {
            addExploreCond("not GUILD_ALIVE");
        }
        private void button5_Click(object sender, EventArgs e)
        {
            if (textBox12.Text != "")
                addExploreCond("'" + textBox12.Text + "' in $.name");
        }

        private void button6_Click(object sender, EventArgs e)
        {
            if (textBox13.Text != "")
                addExploreCond("'" + textBox13.Text + "' not in $.name");
        }
        private void button55_Click(object sender, EventArgs e)
        {
            if (!txtCondExplore.Text.EndsWith("|"))
                txtCondExplore.Text += "|";
        }

        /// <summary>
        /// 卖卡选项卡！
        /// </summary>
        private void addSellCond(string cond)
        {
            if (!chkSuperPrefCards.Checked)
                cond = cond.Replace("$.", "card.");
            if (txtCondSell.Text != "")
                txtCondSell.Text += " and ";
            txtCondSell.Text += cond;
        }

        private void btnSellStar_Click(object sender, EventArgs e)
        {
            addSellCond(textBox10.Text + "<=$.star<=" + textBox9.Text);
        }

        private void btnSellLv_Click(object sender, EventArgs e)
        {
            addSellCond(textBox7.Text + "<=$.lv<=" + textBox8.Text);
        }

        private void btnSellPrice_Click(object sender, EventArgs e)
        {
            addSellCond(textBox5.Text + "<=$.price<= " + textBox6.Text);
        }

        private void btnsSellExclude_Click(object sender, EventArgs e)
        {
            addSellCond("$.mid not in [" + textBox11.Text + "]");
        }

        private void chkNoHolo_CheckedChanged(object sender, EventArgs e)
        {
            string _t = "$.holo";
            if (!chkSuperPrefCards.Checked)
                _t = "card.holo";
            if (!chkNoHolo.Checked)
                _t += "not ";
            txtCondSell.Text = txtCondSell.Text.Replace("and " + _t + " and", "").Replace(_t + " and", "").Replace("and " + _t, "").Replace(_t, "");
        }

        /// <summary>
        /// 地区选项卡！
        /// </summary>
        private void addFloorCond(string cond)
        {
            if (!chkSuperPrefFloor.Checked)
                cond = cond.Replace("$.", "floor.");
            if (txtCondFloor.Text != "" && !txtCondFloor.Text.TrimEnd().EndsWith("|"))
                txtCondFloor.Text += " and ";
            txtCondFloor.Text += cond;
        }
        private void button16_Click(object sender, EventArgs e)
        {
            addFloorCond("$.NOT_FINNISHED");
        }
        private void button80_Click(object sender, EventArgs e)
        {
            addFloorCond("$.HAS_FACTOR");
        }

        private void button12_Click(object sender, EventArgs e)
        {
            addFloorCond("FAIRY_ALIVE");
        }

        private void button11_Click(object sender, EventArgs e)
        {
            addFloorCond("not FAIRY_ALIVE");
        }

        private void button74_Click(object sender, EventArgs e)
        {
            addFloorCond("GUILD_ALIVE");
        }

        private void button75_Click(object sender, EventArgs e)
        {
            addFloorCond("not GUILD_ALIVE");
        }
        private void button77_Click(object sender, EventArgs e)
        {
            addFloorCond("(not GUILD_ALIVE and $.IS_GUILD)");
        }

        private void button78_Click(object sender, EventArgs e)
        {
            addFloorCond("(not FAIRY_ALIVE and not $.IS_GUILD)");
        }

        private void button79_Click(object sender, EventArgs e)
        {
            addFloorCond("((not GUILD_ALIVE and $.IS_GUILD) or (not FAIRY_ALIVE and not $.IS_GUILD))");
        }

        private void button57_Click(object sender, EventArgs e)
        {
            if (!txtCondFloor.Text.EndsWith("|"))
                txtCondFloor.Text += "|";
        }

        private void button13_Click(object sender, EventArgs e)
        {
            addFloorCond(textBox15.Text + "<=$.cost<=" + textBox14.Text);
        }
        /// <summary>
        /// 因子战选项卡！
        /// </summary>
        private void addFactorCond(string cond)
        {
            if (txtCondFactor.Text != "")
                txtCondFactor.Text += " and ";
            txtCondFactor.Text += cond;
        }

        private void button19_Click(object sender, EventArgs e)
        {
            addFactorCond(textBox22.Text + "<=star<=" + textBox21.Text);

        }

        private void button15_Click(object sender, EventArgs e)
        {
            addFactorCond("cid in [" + textBox16.Text + "]");
        }
        /// <summary>
        /// 妖精选项卡！
        /// </summary>
        private void addFairyCond(string cond)
        {
            if (!chkSuperPrefFairy.Checked)
                cond = cond.Replace("$.", "fairy.");
            if (lblFairyCache.Text != "")
                lblFairyCache.Text += " and ";
            lblFairyCache.Text += cond;
        }
        private void button22_Click(object sender, EventArgs e)
        {
            if (txtCondFairy.Text != "")
                txtCondFairy.Text += " or ";
            txtCondFairy.Text += "(" + lblFairyCache.Text + ")";
            lblFairyCache.Text = "";
            button23.Enabled = true;
            button24.Enabled = true;
            button25.Enabled = true;
            button26.Enabled = true;
            button47.Enabled = true;
            button46.Enabled = true;
            button27.Enabled = true;
            button56.Enabled = true;
            button62.Enabled = true;
        }

        private void button26_Click(object sender, EventArgs e)
        {
            addFairyCond("$.NOT_BATTLED");
            button26.Enabled = false;
            button47.Enabled = false;
        }
        private void button47_Click(object sender, EventArgs e)
        {
            addFairyCond("not $.NOT_BATTLED");
            button47.Enabled = false;
            button26.Enabled = false;
        }

        private void button25_Click(object sender, EventArgs e)
        {
            addFairyCond("$.IS_MINE");
            button25.Enabled = false;
            button46.Enabled = false;
        }
        private void button46_Click(object sender, EventArgs e)
        {
            addFairyCond("not $.IS_MINE");
            button46.Enabled = false;
            button25.Enabled = false;
        }

        private void button24_Click(object sender, EventArgs e)
        {
            addFairyCond("$.IS_WAKE");
            button24.Enabled = false;
            button27.Enabled = false;
            button56.Enabled = false;
        }
        private void button27_Click(object sender, EventArgs e)
        {
            addFairyCond("not $.IS_WAKE");
            button27.Enabled = false;
            button24.Enabled = false;
            button56.Enabled = false;
        }

        private void button62_Click(object sender, EventArgs e)
        {
            addFairyCond("$.IS_GUILD");
            button62.Enabled = false;
        }

        private void button56_Click(object sender, EventArgs e)
        {
            addFairyCond("$.IS_WAKE_RARE");
            button27.Enabled = false;
            button24.Enabled = false;
            button56.Enabled = false;
        }
        private void button23_Click(object sender, EventArgs e)
        {
            addFairyCond("$.LIMIT<" + (int.Parse(textBox17.Text) * 3600 + int.Parse(textBox18.Text) * 60 + int.Parse(textBox19.Text)));
            button23.Enabled = false;
        }
        private void button21_Click(object sender, EventArgs e)
        {
            lblFairyCache.Text = "";
            button23.Enabled = true;
            button24.Enabled = true;
            button25.Enabled = true;
            button26.Enabled = true;
            button47.Enabled = true;
            button46.Enabled = true;
            button27.Enabled = true;
            button56.Enabled = true;
            button62.Enabled = true;
        }
        /// <summary>
        /// 卡组选项卡！
        /// </summary>
        private void addCarddeckCond(string cond)
        {
            if (!chkSuperPrefCarddeck.Checked)
                cond = cond.Replace("$.", "fairy.");
            if (lblCarddeckCache.Text != "")
                lblCarddeckCache.Text += " and ";
            lblCarddeckCache.Text += cond;
        }
        private void button36_Click(object sender, EventArgs e)
        {
            addCarddeckCond(textBox27.Text + "<=$.lv<=" + textBox26.Text);
            button36.Enabled = false;
        }

        private void button35_Click(object sender, EventArgs e)
        {
            addCarddeckCond(textBox24.Text + "<=$.hp<=" + textBox25.Text);
            button35.Enabled = false;
        }
        private void button76_Click(object sender, EventArgs e)
        {
            addCarddeckCond(float.Parse(textBox23.Text)/100 + "<=$.hp%<=" + float.Parse(textBox33.Text)/100);
            button76.Enabled = false;
        }
        private void button37_Click(object sender, EventArgs e)
        {
            addCarddeckCond("BC>" + textBox32.Text);
            button37.Enabled = false;
        }

        private void button30_Click(object sender, EventArgs e)
        {
            addFairyCond("$.LIMIT<" + (int.Parse(textBox31.Text) * 3600 + int.Parse(textBox30.Text) * 60 + int.Parse(textBox29.Text)));
            button30.Enabled = false;
        }



        private void button34_Click(object sender, EventArgs e)
        {
            addCarddeckCond("not FAIRY_ALIVE");
            button34.Enabled = false;
            button33.Enabled = false;
        }

        private void button33_Click(object sender, EventArgs e)
        {
            addCarddeckCond("FAIRY_ALIVE");
            button33.Enabled = false;
            button34.Enabled = false;
        }
        private void button72_Click(object sender, EventArgs e)
        {
            addCarddeckCond("GUILD_ALIVE");
            button72.Enabled = false;
            button73.Enabled = false;
        }

        private void button73_Click(object sender, EventArgs e)
        {
            addCarddeckCond("not GUILD_ALIVE");
            button72.Enabled = false;
            button73.Enabled = false;
        }

        private void button32_Click(object sender, EventArgs e)
        {
            addCarddeckCond("$.IS_MINE");
            button32.Enabled = false;
            button49.Enabled = false;
        }

        private void button49_Click(object sender, EventArgs e)
        {
            addCarddeckCond("not $.IS_MINE");
            button49.Enabled = false;
            button32.Enabled = false;
        }

        private void button31_Click(object sender, EventArgs e)
        {
            addCarddeckCond("$.IS_WAKE");
            button31.Enabled = false;
            button48.Enabled = false;
            button58.Enabled = false;
        }
        private void button48_Click(object sender, EventArgs e)
        {
            addCarddeckCond("not $.IS_WAKE");
            button48.Enabled = false;
            button31.Enabled = false;
            button58.Enabled = false;
        }

        private void button58_Click(object sender, EventArgs e)
        {
            addCarddeckCond("$.IS_WAKE_RARE");
            button48.Enabled = false;
            button31.Enabled = false;
            button58.Enabled = false;
        }

        private void button63_Click(object sender, EventArgs e)
        {
            addCarddeckCond("$.IS_GUILD");
            button63.Enabled = false;
        }

        private void button29_Click(object sender, EventArgs e)
        {
            if (lblCarddeckCache.Text != "")
            {
                if (cboDeckList.Text == "")
                {
                    cboDeckList.Focus();
                    return;
                }
                if (textBox20.Text == "")
                {
                    textBox20.Focus();
                    return;
                }
                if (cboDeckList.Items.IndexOf(cboDeckList.Text) == -1 && 
                    !cboDeckList.Text.StartsWith("auto_set") &&
                    cboReservedName.SelectedIndex == 0 &&
                (MessageBox.Show("卡组名不存在，是否继续添加？\n你也可以稍后添加卡组" + cboDeckList.Text, "呵呵", MessageBoxButtons.YesNo, MessageBoxIcon.Exclamation) == DialogResult.No))
                    return;
                if (txtCondCarddeck.Text == "")
                    txtCondCarddeck.Text = "'" + textBox20.Text + "'";
                if (cboDeckList.Text == "auto_set")
                    cboDeckList.Text = "auto_set()";
                txtCondCarddeck.Text =
                    txtCondCarddeck.Text.Replace(" or '" + textBox20.Text + "'", " or ('" + textBox20.Text + "')");
                txtCondCarddeck.Text =
                    txtCondCarddeck.Text.Replace("'" + textBox20.Text + "'",
                    "(" + lblCarddeckCache.Text + ") and '" + cboDeckList.Text + "' or '" + textBox20.Text + "'");

                lblCarddeckCache.Text = "";
                button35.Enabled = true;
                button36.Enabled = true;
                button37.Enabled = true;
                button30.Enabled = true;
                button34.Enabled = true;
                button33.Enabled = true;
                button32.Enabled = true;
                button31.Enabled = true;
                button48.Enabled = true;
                button49.Enabled = true;
                button58.Enabled = true;
                button63.Enabled = true;
                button72.Enabled = true;
                button73.Enabled = true;
                button76.Enabled = true;
                cboReservedName.SelectedIndex = 0;
            }
        }

        private void button28_Click(object sender, EventArgs e)
        {
            lblCarddeckCache.Text = "";
            button35.Enabled = true;
            button36.Enabled = true;
            button37.Enabled = true;
            button30.Enabled = true;
            button34.Enabled = true;
            button33.Enabled = true;
            button32.Enabled = true;
            button31.Enabled = true;
            button48.Enabled = true;
            button49.Enabled = true;
            button58.Enabled = true;
            button63.Enabled = true;
            button72.Enabled = true;
            button73.Enabled = true;
            button76.Enabled = true;
            cboReservedName.SelectedIndex = 0;
        }

        private void button20_Click(object sender, EventArgs e)
        {
            if (cboCfgFile.Items.Count == 0)
                return;
            saveAll();
            saveCond();
            refreshAll();
        }

        private void button38_Click(object sender, EventArgs e)
        {
            if (cboCfgFile.Items.Count == 0)
                return;
            refreshAll();
            refreshCond();
        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            System.Diagnostics.Process.Start("https://github.com/fffonion/MAClient/wiki/%E5%85%B3%E4%BA%8E%E5%8D%A1%E7%BB%84%E5%92%8C%E9%85%8D%E5%8D%A1");
        }
        /// <summary>
        /// 清除
        /// </summary>
        private void button39_Click(object sender, EventArgs e)
        {
            txtCondTasker.Text = "";
        }

        private void button40_Click(object sender, EventArgs e)
        {
            txtCondFairy.Text = "";
        }

        private void button41_Click(object sender, EventArgs e)
        {
            txtCondExplore.Text = "";
        }

        private void button42_Click(object sender, EventArgs e)
        {
            txtCondFloor.Text = "";
        }

        private void button43_Click(object sender, EventArgs e)
        {
            txtCondCarddeck.Text = "";
        }

        private void button44_Click(object sender, EventArgs e)
        {
            txtCondFactor.Text = "";
        }

        private void button45_Click(object sender, EventArgs e)
        {
            txtCondSell.Text = "";
        }
        private bool check_path_valid(string path)
        {
            for (int i = 0; i < path.Length; i++)
            {
                if (Convert.ToInt32(Convert.ToChar(path.Substring(i, 1))) > Convert.ToInt32(Convert.ToChar(128)))
                {
                    return false;
                }
            }
            return true;
        }
        private void start_mac(string arg = "")
        {
            string cfgpath = cboCfgFile.Text;
            if (!File.Exists(maclient_path))
            {
                if (MessageBox.Show("当前目录下木有maclient_cli.exe或maclient_cli.py，是否手动寻找？", "呵呵", MessageBoxButtons.YesNo, MessageBoxIcon.Error) == DialogResult.Yes)
                {
                    OpenFileDialog fileDialog1 = new OpenFileDialog();
                    fileDialog1.Filter = "maclient_cli.exe,maclient_cli.py|*.exe;*.py";
                    fileDialog1.FilterIndex = 1;
                    fileDialog1.RestoreDirectory = true;
                    if (fileDialog1.ShowDialog() == DialogResult.OK)
                    {
                        maclient_path = fileDialog1.FileName;
                    }
                    else
                    {
                        return;
                    }

                }
                else
                {
                    return;
                }

            }
            if (!check_path_valid(maclient_path))
            {
                MessageBox.Show("路径中包含非英文/数字，maclient可能无法启动", "呵呵", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (cfgpath == "" || !File.Exists(cfgpath))
            {
                if (MessageBox.Show("木有发现配置文件，是否手动寻找？", "呵呵", MessageBoxButtons.YesNo, MessageBoxIcon.Error) == DialogResult.Yes)
                {
                    OpenFileDialog fileDialog1 = new OpenFileDialog();
                    fileDialog1.Filter = "config.ini|*.ini";
                    fileDialog1.FilterIndex = 1;
                    fileDialog1.RestoreDirectory = true;
                    if (fileDialog1.ShowDialog() == DialogResult.OK)
                    {
                        if (cboCfgFile.FindStringExact(fileDialog1.FileName) == -1)
                        {
                            if (fileDialog1.FileName.IndexOf(":") == -1)
                                cboCfgFile.Items.Add(System.Environment.CurrentDirectory + "\\" + fileDialog1.FileName);
                            else
                                cboCfgFile.Items.Add(fileDialog1.FileName);
                            cboCfgFile.SelectedIndex = cboCfgFile.FindStringExact(fileDialog1.FileName);
                        }

                        cfgpath = fileDialog1.FileName;
                    }
                    else
                    {
                        return;
                    }

                }
                else
                {
                    return;
                }

            }
            //cboCfgFile.SelectedIndex = 0;
            if (chkUseNiceTerm.Checked)
            {
                frmNiceTerm f = new frmNiceTerm();
                f.Show();
                niceterms.Add(f);
                int _cur = niceterms.Count;
                f.kill_callback = () => niceterms.RemoveAt(_cur - 1);
                if(maclient_path.EndsWith("py"))
                    f.StartProcess("python.exe", maclient_path+" \"" + cfgpath + "\" " + arg);
                else
                    f.StartProcess(maclient_path, "\"" + cfgpath + "\" " + arg);
            }
            else
            {
                Process proc = new Process();
                proc.StartInfo.FileName = maclient_path;
                proc.StartInfo.CreateNoWindow = true;
                proc.StartInfo.UseShellExecute = true;
                proc.StartInfo.Arguments = "\"" + cfgpath + "\" " + arg;
                proc.EnableRaisingEvents = true;
                proc.Start();
            }

        }
        private void button3_Click(object sender, EventArgs e)
        {
            start_mac();
        }

        private void button10_Click(object sender, EventArgs e)
        {
            if (cbTask.Items.Count == 0)
            {
                MessageBox.Show("不存在的任务名，请检查后重试！", "呵呵", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            start_mac("t:" + cbTask.Items[cbTask.SelectedIndex].ToString());
        }

        private void button14_Click(object sender, EventArgs e)
        {
            start_mac("e");
        }

        private void button50_Click(object sender, EventArgs e)
        {
            start_mac("fcb");
        }

        private void button51_Click(object sender, EventArgs e)
        {
            start_mac("fyb");
        }

        private void label41_Click(object sender, EventArgs e)
        {
            //tabControl1.SelectedIndex=0;
            cbTask.Focus();
        }

        private void btnSaveAs_Click(object sender, EventArgs e)
        {
            if (cboCfgFile.Items.Count == 0)
                return;
            SaveFileDialog fileDialog1 = new SaveFileDialog();
            fileDialog1.Filter = "配置文件(*.ini)|*.ini|所有文件(*.*)|*.*";
            fileDialog1.FilterIndex = 1;
            fileDialog1.RestoreDirectory = true;
            if (fileDialog1.ShowDialog() == DialogResult.OK)
            {
                System.IO.File.Copy(cboCfgFile.Text, fileDialog1.FileName, true);
                cf = new configParser(fileDialog1.FileName);
                saveAll();
                saveCond();
                cboCfgFile.Items.Add(fileDialog1.FileName);
                cboCfgFile.SelectedIndex = cboCfgFile.FindStringExact(fileDialog1.FileName);
            }
        }

        private void txtCondFairy_Leave(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondFairy, 137);
            a.ChangeOffsetY(button40, -363);
        }

        private void txtCondFairy_Enter(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondFairy, 500);
            a.ChangeOffsetY(button40, 363);
        }

        private void txtCondExplore_Enter(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondExplore, 500);
            a.ChangeOffsetY(button41, 363);
        }

        private void txtCondExplore_Leave(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondExplore, 137);
            a.ChangeOffsetY(button41, -363);
        }

        private void txtCondFloor_Enter(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondFloor, 500);
            a.ChangeOffsetY(button42, 363);
        }

        private void txtCondFloor_Leave(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondFloor, 137);
            a.ChangeOffsetY(button42, -363);
        }

        private void txtCondFactor_Leave(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondFactor, 137);
            a.ChangeOffsetY(button44, -363);
        }

        private void txtCondFactor_Enter(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondFactor, 500);
            a.ChangeOffsetY(button44, 363);
        }

        private void txtCondSell_Enter(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondSell, 500);
            a.ChangeOffsetY(button45, 363);
        }

        private void txtCondSell_Leave(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondSell, 137);
            a.ChangeOffsetY(button45, -363);
        }

        private void txtCondTasker_Leave(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondTasker, 137);
            a.ChangeOffsetY(label41, -363);
            a.ChangeOffsetY(button39, -363);
        }

        private void txtCondTasker_Enter(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondTasker, 500);
            a.ChangeOffsetY(label41, 363);
            a.ChangeOffsetY(button39, 363);
        }

        private void txtCondCarddeck_Enter(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondCarddeck, 500);
            a.ChangeOffsetY(button43, 363);
        }

        private void txtCondCarddeck_Leave(object sender, EventArgs e)
        {
            CtrlAnimator a = new CtrlAnimator(this);
            a.ChangeHeight(txtCondCarddeck, 137);
            a.ChangeOffsetY(button43, -363);
        }

        private void button60_Click(object sender, EventArgs e)
        {
            txtCondExplore.Text += " or ";
        }

        private void button59_Click(object sender, EventArgs e)
        {
            WndHdl.WndInfo[] res = WndHdl.findHwndbyTitleReg(@"\[[^\]]+\] AP\:");
            if (button59.Text.StartsWith("隐藏"))
            {
                WndHdl.hideWnd(res);
                button59.Text = "恢复";
            }
            else
            {
                WndHdl.showWnd(res);
                button59.Text = "隐藏";
            }
        }

        private ToolStripMenuItem menuItem(string title, EventHandler click = null, WndHdl.WndInfo? winfo = null, Image img = null)
        {
            ToolStripMenuItem i = new ToolStripMenuItem();
            i.Text = title;
            if (click != null) i.Click += click;
            if (winfo != null) i.Tag = winfo;
            if (img != null) i.Image = img;
            return i;
        }

        private void load_menu()
        {
            WndHdl.WndInfo[] res = WndHdl.findHwndbyTitleReg(@"\[[^\]]+\] AP\:");
            //set on EVENT_CHANGE hook
            thook th = new thook(WinEventProc);
            Thread oThread = new Thread(new ThreadStart(th.threading_hook));
            oThread.Start();
            //WndHdl.WndInfo[] res = WndHdl.findHwndbyTitleReg(@"ebug");
            foreach (WndHdl.WndInfo r in res)
            {
                ToolStripMenuItem itm = menuItem("", new EventHandler(delegate(Object o, EventArgs a)
                {
                    if (WndHdl.isVisible(r.hwnd)) WndHdl.hideWnd(r);
                    else { WndHdl.showWnd(r); WndHdl.SetForegroundWindow(r.hwnd); }
                }), r);
                //MessageBox.Show(((uint)r.procid).ToString() + ";" + ((uint)r.threadid).ToString());
                itm.Font = new Font(textBox1.Font, FontStyle.Bold);
                itm.ToolTipText = "切换显示/隐藏";
                dockMenu.Items.Add(itm);
                dockMenu.Items.Add(new ToolStripTextBoxEx(Color.FromArgb(128, 0, 128, 0)));//AP
                dockMenu.Items.Add(new ToolStripTextBoxEx(Color.FromArgb(128, 128, 0, 0)));//BC
                ToolStripMenuItem t = menuItem("");//G,FP
                t.Enabled = false;
                dockMenu.Items.Add(t);
                dockMenu.Items.Add(new ToolStripSeparator());
            }
            //ToolStripTextBoxEx t = new ToolStripTextBoxEx();
            dockMenu.Items.Add(menuItem(button59.Text + "全部", new EventHandler(delegate(Object o, EventArgs a)
            {
                button59_Click(o, a); ToolStripMenuItem m = o as ToolStripMenuItem; m.Text = button59.Text + "全部";
            })));
            dockMenu.Items.Add(menuItem("显示GUI", new EventHandler(this.frmNormalize)));
            dockMenu.Items.Add(menuItem("退出", new EventHandler(delegate(Object o, EventArgs a)
            {
                notifyIcon1.Visible = false;
                button59.Text = "恢复"; button59_Click(o, a);
                System.Environment.Exit(0);
            })));
            repaint_menu();
        }


        Regex bscsplt = new Regex(@"\[([^\[]+)\] ");
        public void WinEventProc(IntPtr hWinEventHook, uint eventType,
            IntPtr hwnd, int idObject, int idChild, uint dwEventThread, uint dwmsEventTime)
        {
            // filter out non-HWND namechanges... (eg. items within a listbox)
            if (idObject != 0 || idChild != 0)
            {
                return;
            }
            StringBuilder sb = new StringBuilder(256);
            WndHdl.GetWindowTextW(hwnd, sb, sb.Capacity);
            if (bscsplt.IsMatch(sb.ToString()))
                repaint_menu();
            //int a;
            //WndHdl.GetWindowThreadProcessId(hwnd, out a);
            //MessageBox.Show(sb.ToString() + ";"+a);
        }

        Regex fullsplt = new Regex(@"\[([^\[]+)\] AP\:([\d\/]+) BC\:([\d\/]+) G\:(\d+) F\:(\d+) SP\:(\d+) 卡片\:(\d+)\s{0,1}(.*)");
        Regex splt = new Regex(@"(\d+)\/(\d+)");

        private void repaint_menu()
        {
            string txtnot = "MAClient users";
            for (int i = 2; i < dockMenu.Items.Count - 3; i += 5)
            {
                dockMenu.Items[i].Tag = WndHdl.refreshTitle((WndHdl.WndInfo)dockMenu.Items[i].Tag);
                string title = ((WndHdl.WndInfo)dockMenu.Items[i].Tag).title;
                if (title == "")//closed
                {
                    for (int j = 0; j < 5; j++)
                        dockMenu.Items.RemoveAt(i);
                    i -= 5;
                    continue;
                }
                GroupCollection g = fullsplt.Match(title).Groups;
                dockMenu.Items[i].Text = g[1].ToString();
                for (int j = 1; j < 3; j++)
                {
                    GroupCollection g2 = splt.Match(g[1 + j].ToString()).Groups;
                    float p = float.Parse(g2[1].ToString()) / float.Parse(g2[2].ToString());
                    ((ToolStripTextBoxEx)dockMenu.Items[i + j]).setPercent(p);
                    dockMenu.Items[i + j].Text = g[1 + j].ToString();
                }
                //+ g[4] + "  基:" + g[5]
                dockMenu.Items[i + 3].Text = "金:" + g[4] + " 卡片:" + g[7];
                txtnot += Environment.NewLine + "❁" + g[1];
            }
            this.notifyIcon1.Text = txtnot;
        }

        private bool has_show_bollon = false;
        private void frmConfig_Resize(object sender, EventArgs e)
        {
            if (FormWindowState.Minimized == WindowState)
            {
                this.Hide();
                this.ShowInTaskbar = false;
                notifyIcon1.Visible = true;

                if (!has_show_bollon)
                {
                    notifyIcon1.ShowBalloonTip(1);
                    has_show_bollon = true;
                }
                if (button59.Text.StartsWith("隐藏"))
                    button59_Click(sender, e);
                if (dockMenu.Items.Count <= 2) load_menu();
            }

        }

        private void frmNormalize(Object o, EventArgs a)
        {
            frmNormalize();
        }

        private void frmNormalize()
        {
            this.Show();
            WindowState = FormWindowState.Normal;
            this.Activate();
            this.ShowInTaskbar = true;
            notifyIcon1.Visible = false;
        }




        private void button60_Click_1(object sender, EventArgs e)
        {
            /*WinEventDelegate procDelegate = new WinEventDelegate(WinEventProc);
            // Listen for name change changes across all processes/threads on current desktop...
            IntPtr hhook = SetWinEventHook(EVENT_OBJECT_NAMECHANGE, EVENT_OBJECT_NAMECHANGE, IntPtr.Zero,
                    procDelegate, 0, 0, WINEVENT_OUTOFCONTEXT);
            MessageBox.Show("Tracking name changes on HWNDs, close message box to exit.");

            UnhookWinEvent(hhook);*/
        }

        private void frmConfig_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (niceterms.Count > 0){
                if (MessageBox.Show("在终端模拟器中还运行着" + niceterms.Count + "个MAClient，退出后将终止他们的运行\n红豆泥要继续嘛？","咦",MessageBoxButtons.YesNo,MessageBoxIcon.Exclamation)==DialogResult.Yes)
                {
                    foreach (frmNiceTerm nt in niceterms)
                    {
                        if (nt.process != null && !nt.process.HasExited)
                        {
                            nt.process.Kill();
                            nt.outputWorker.CancelAsync();
                        }
                    }
                }else{
                    e.Cancel=true;
                    return;
                }
            }
            WndHdl.WndInfo[] res = WndHdl.findHwndbyTitleReg(@"\[[^\]]+\] AP\:");
            WndHdl.showWndIfHided(res);
            Process.GetCurrentProcess().Kill();
            //System.Environment.Exit(0);
        }


        private void button60_Click_2(object sender, EventArgs e)
        {
            if (!groupBox11.Enabled)//左边group设为可用
            {
                cboDeckList.Text = "auto_set";
                cboAim.SelectedIndex = cboAim.SelectedIndex == -1 ? 0 : cboAim.SelectedIndex;
                cboBCLimit.SelectedIndex = cboBCLimit.SelectedIndex == -1 ? 0 : cboBCLimit.SelectedIndex;
                cboLineCnt.SelectedIndex = cboLineCnt.SelectedIndex == -1 ? 0 : cboLineCnt.SelectedIndex;
                button60.Font = new Font(button60.Font, FontStyle.Bold); 
                button60.Text = "←←确认参数";
            }
            else//确认
            {
                cboDeckList.Text = "";
                switch (cboBCLimit.SelectedIndex)
                {
                    case 1:
                        cboDeckList.Text += " bc:max";
                        break;
                    case 2:
                        cboDeckList.Text += " bc:" + txtBCLimit.Text;
                        break;
                }
                if (cboLineCnt.SelectedIndex != 0)
                    cboDeckList.Text += " line:" + (cboLineCnt.SelectedIndex + 1).ToString();
                switch (cboAim.SelectedIndex)
                {
                    case 1:
                        cboDeckList.Text += " aim:MAX_CP";
                        break;
                    case 2:
                        cboDeckList.Text += " aim:DEFEAT";
                        break;
                }
                if (!chkIsTest.Checked)
                    cboDeckList.Text += " notest";
                if (!chkIsFast.Checked)
                    cboDeckList.Text += " nofast";
                if (txtCardEval.Text != "$.lv>=45")
                    cboDeckList.Text += " sel:" + txtCardEval.Text;
                if (txtCardIncl.Text != "")
                    cboDeckList.Text += " incl:" + txtCardIncl.Text;
                cboDeckList.Text = "auto_set(" + cboDeckList.Text.Trim() + ")";
                button60.Font = new Font(button60.Font, FontStyle.Regular); 
                button60.Text = "使用自动配卡";
            }
            groupBox11.Enabled = !groupBox11.Enabled;

        }

        private void cboBCLimit_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cboBCLimit.SelectedIndex == 2) txtBCLimit.Enabled = true;
            else txtBCLimit.Enabled = false;
        }

        private void checkWarning()
        {
            if ((cboLineCnt.SelectedIndex > 0 && cboAim.SelectedIndex == 2) ||//超过一排，击败妖精
                    (cboLineCnt.SelectedIndex == 2 && !chkIsFast.Checked))//三排，非快速模式
                lblLineWarning.Visible = true;
            else lblLineWarning.Visible = false;
        }

        private void cboLineCnt_SelectedIndexChanged(object sender, EventArgs e)
        {
            checkWarning();
        }

        private void chkIsTest_CheckedChanged(object sender, EventArgs e)
        {
            if (chkIsTest.Checked)
                chkIsTest.ForeColor = Color.Red;
            else
                chkIsTest.ForeColor = Color.Black;
        }

        private void cboAim_SelectedIndexChanged(object sender, EventArgs e)
        {
            checkWarning();
        }

        private void chkIsFast_CheckedChanged(object sender, EventArgs e)
        {
            checkWarning();
        }

        bool has_load_plugins = false;
        private void tabControl1_Click(object sender, EventArgs e)
        {
            if (tabControl1.SelectedIndex == 1 && !has_load_plugins)
                loadPluginList();
        }

        private void loadPluginList()
        {
            if (cboCfgFile.Items.Count == 0)
                loadPluginList(Path.Combine(System.Environment.CurrentDirectory, "plugins"));
            else
                loadPluginList(Path.Combine(Path.GetDirectoryName(cboCfgFile.SelectedItem.ToString()), "plugins"));
        }
        private void loadPluginList(string pluginPath)
        {
            if (chkUsePlugins.Checked)
            {
                label70.Text = "开启";
                label70.ForeColor = Color.ForestGreen;
                label71.Visible = true;
                label72.Visible = true;
                label73.Visible = true;
                label74.Visible = true;
                label75.Visible = true;
                label76.Visible = true;
                label77.Visible = true;
                label78.Visible = true;
                label79.Visible = true;
                label82.Visible = true;
                label83.Visible = true;
                label84.Visible = true;
                lblPluginState.Visible = true;
            }
            else
            {
                label70.Text = "关闭";
                label70.ForeColor = Color.OrangeRed;
                label71.Visible = false;
                label72.Visible = false;
                label73.Visible = false;
                label74.Visible = false;
                label75.Visible = false;
                label76.Visible = false;
                label77.Visible = false;
                label78.Visible = false;
                label79.Visible = false;
                label82.Visible = false;
                label83.Visible = false;
                label84.Visible = false;
                lblPluginState.Visible = false;
                return;
            }
            DirectoryInfo folder = new DirectoryInfo(pluginPath);
            if (!folder.Exists)
                return;
            lstPlugins.Items.Clear();
            pluginItem pi;
            string line;
            List<string> has_read = new List<string>();
            foreach (FileInfo file in folder.GetFiles("*.py?"))
            {
                string fn = file.ToString().Substring(0, file.ToString().Length - file.Extension.Length);
                string fext = file.Extension.Substring(1);
                if (has_read.IndexOf(fn) != -1 && file.Extension == ".pyc")
                    continue;
                has_read.Add(fn);
                pi = new pluginItem();
                pi.file_name = fn;
                pi.file_ext = fext;
                if (file.Extension == ".py")
                {
                    StreamReader fr = new StreamReader(Path.Combine(pluginPath, file.ToString()));
                    bool _unfinished_extra_cmd = false;
                    bool _unfinished_hooks = false;
                    while ((line = fr.ReadLine()) != null)
                    {
                        if (_unfinished_hooks)
                        {
                            pi.hooks += line.Trim().Replace("'", "").Replace("\"", "")
                                .Replace("{", "").Replace("}", "");
                            _unfinished_hooks = !line.EndsWith("}");
                        }
                        if (_unfinished_extra_cmd)
                        {
                            pi.extra_cmd += line.Trim().Replace("'", "").Replace("\"", "")
                                .Replace("{", "").Replace("}", "");
                            _unfinished_extra_cmd = !line.EndsWith("}");
                        }
                        if (line.StartsWith("__version__"))
                            pi.version = "v" + line.Split('=')[1].Trim();
                        else if (line.StartsWith("__plugin_name__"))
                            pi.plugin_name = line.Split('=')[1].Trim().Replace("'", "").Replace("\"", "");
                        else if (line.StartsWith("__author"))
                            pi.author = line.Split('=')[1].Trim().Replace("'", "").Replace("\"", "");
                        else if (line.StartsWith("__tip__"))
                            pi.tip = line.Split('=')[1].Trim().Replace("'", "").Replace("\"", "");
                        else if (line.StartsWith("hooks"))
                        {
                            pi.hooks = line.Split('=')[1].Trim().Replace("'", "").Replace("\"", "")
                                .Replace("{", "").Replace("}", "");
                            _unfinished_hooks = !line.EndsWith("}");
                        }
                        else if (line.StartsWith("extra_cmd"))
                        {
                            pi.extra_cmd = line.Split('=')[1].Trim().Replace("'", "").Replace("\"", "")
                                .Replace("{", "").Replace("}", "");
                            _unfinished_extra_cmd = !line.EndsWith("}");
                        }
                        else if (line.IndexOf("end meta") != -1)
                            break;
                    }
                    fr.Close();
                }
                lstPlugins.Items.Add(pi);
            }
            if (lstPlugins.Items.Count > 0)
                lstPlugins.SelectedIndex = 0;
        }

        private void lstPlugins_DrawItem(object sender, DrawItemEventArgs e)
        {
            if (lstPlugins.Items.Count == 0)
                return;
            e.DrawBackground();
            Graphics g = e.Graphics;
            pluginItem item = (pluginItem)lstPlugins.Items[e.Index];
            Brush brush;
            bool selected = false;
            if ((e.State & DrawItemState.Selected) == DrawItemState.Selected)
            {
                brush = new SolidBrush(Color.FromArgb(0x8e, 0x44, 0xad));
                selected = true;
            }
            else
                brush = (e.Index) % 2 == 1 ? Brushes.LightGray : new SolidBrush(e.BackColor);
            g.FillRectangle(brush, e.Bounds);
            //name
            e.Graphics.DrawString(item.file_name,
                        new System.Drawing.Font("微软雅黑", 10F, System.Drawing.FontStyle.Bold),
                        new SolidBrush(e.ForeColor), 0, e.Bounds.Top, StringFormat.GenericDefault);
            //version
            e.Graphics.DrawString(item.version,
                        new System.Drawing.Font("微软雅黑", 7F, System.Drawing.FontStyle.Regular),
                        selected ? Brushes.AntiqueWhite : Brushes.Firebrick, e.Bounds.Width - 33, e.Bounds.Top, StringFormat.GenericDefault);
            //plugin name
            e.Graphics.DrawString(item.plugin_name, e.Font,
                        selected ? Brushes.White : Brushes.DimGray, 0, e.Bounds.Bottom - 23, StringFormat.GenericDefault);
            //ext
            e.Graphics.DrawString("[" + item.file_ext + "]",
                        new System.Drawing.Font("微软雅黑", 9.2F, System.Drawing.FontStyle.Bold),
                        selected ? Brushes.LightYellow : Brushes.Gold, e.Bounds.Width - 38, e.Bounds.Bottom - 23, StringFormat.GenericDefault);
            e.DrawFocusRectangle();
        }

        private void button64_Click(object sender, EventArgs e)
        {
            loadPluginList();
        }

        private void button65_Click(object sender, EventArgs e)
        {
            string placeholder = "就决定是这里了";
            SaveFileDialog sf = new SaveFileDialog();
            sf.Title = "选择插件目录";
            sf.FileName = placeholder;
            sf.RestoreDirectory = true;
            sf.OverwritePrompt = false;
            sf.CreatePrompt = false;
            sf.Filter = "文件夹|*.";
            if (sf.ShowDialog() == DialogResult.OK)
            {
                loadPluginList(Path.GetDirectoryName(sf.FileName));
            }
        }

        private void lstPlugins_SelectedIndexChanged(object sender, EventArgs e)
        {
            pluginItem item = (pluginItem)lstPlugins.SelectedItem;
            label71.Text = item.file_name;
            label72.Text = item.plugin_name;
            if (item.version == null || item.file_name.StartsWith("_"))
            {
                label73.Visible = false;
                label74.Visible = false;
                label75.Visible = false;
                label76.Visible = false;
                label77.Visible = false;
                label78.Visible = false;
                label79.Visible = false;
                label82.Visible = false;
                label83.Text = item.file_name.StartsWith("_") ? "依赖模块" : "非源代码无法获得详细信息";
            }
            else
            {
                label73.Visible = true;
                label74.Visible = true;
                label75.Visible = true;
                label76.Visible = true;
                label77.Visible = true;
                label78.Visible = true;
                label79.Visible = true;
                label82.Visible = true;
                label73.Text = item.version;
                label79.Text = item.author;
                label83.Text = item.tip == null ? "无" : item.tip;
                //hooks
                //max 11
                int cnt = 0;
                string[] l = item.hooks.Split(',');
                if (l.Length > 0 && l[0] != "")
                {
                    label75.Text = "";
                    foreach (string v in l)
                    {
                        if (label75.Text.Length > 0)
                            label75.Text += "\n";
                        if (cnt == 10 && l.Length > 11)
                        {
                            label75.Text += "……等" + l.Length + "项";
                            break;
                        }
                        string[] p = v.Trim().Split(':');
                        if (p.Length < 2)
                            continue;
                        label75.Text += p[0].Replace("ENTER_", "进入").Replace("EXIT_", "退出") + " 级别" + p[1];
                        cnt++;
                    }
                }
                else
                    label75.Text = "无";
                //extra_cmd
                //max 11
                l = item.extra_cmd.Split(',');
                if (l.Length > 0 && l[0] != "")
                {
                    Dictionary<string, string> cmds = new Dictionary<string, string>();
                    label76.Text = "";
                    foreach (string v in l)
                    {
                        if (cmds.Count == 10 && l.Length > 11)
                        {
                            cmds.Add("……等" + l.Length + "项", "");
                            break;
                        }
                        string[] p = v.Trim().Split(':');
                        if (p.Length < 2)
                            continue;
                        if (cmds.ContainsKey(p[1]))
                        {
                            string old = cmds[p[1]];
                            if (old.Length > p[0].Length)
                                cmds[p[1]] = old + "\n    缩写:" + p[0];
                            else
                                cmds[p[1]] = p[0] + "\n    缩写:" + old;
                        }
                        else
                            cmds.Add(p[1], p[0]);
                    }
                    foreach (string c in cmds.Values)
                    {
                        label76.Text += c + "\n";
                    }
                }
                else
                    label76.Text = "无";
                if (txtDisabledPlugins.Text.IndexOf(item.file_name) != -1)
                {
                    lblPluginState.Text = "×";
                    lblPluginState.ForeColor = Color.Crimson;
                    btnToggleEnable.ForeColor = Color.Green;
                    btnToggleEnable.Text = "启用当前";
                }
                else
                {
                    if (item.file_name.StartsWith("_"))
                    {
                        lblPluginState.Text = "○";
                        lblPluginState.ForeColor = Color.Goldenrod;
                    }
                    else
                    {
                        lblPluginState.Text = "√";
                        lblPluginState.ForeColor = Color.Green;
                    }
                    btnToggleEnable.ForeColor = Color.Crimson;
                    btnToggleEnable.Text = "禁用当前";
                }
            }
        }

        private void btnToggleEnable_Click(object sender, EventArgs e)
        {
            if (label70.Text == "关闭")
                return;
            if (btnToggleEnable.Text == "启用当前")
            {
                txtDisabledPlugins.Text = txtDisabledPlugins.Text.Replace(label71.Text + ",", "")
                    .Replace("," + label71.Text, "").Replace(label71.Text, "");
                btnToggleEnable.ForeColor = Color.Crimson;
                btnToggleEnable.Text = "禁用当前";
                lblPluginState.Text = "√";
                lblPluginState.ForeColor = Color.Green;
            }
            else
            {
                if (label71.Text.StartsWith("_"))
                {
                    MessageBox.Show("不能禁用依赖模块或过时的插件");
                    return;
                }
                if (txtDisabledPlugins.Text.Length > 0)
                    txtDisabledPlugins.Text += ",";
                txtDisabledPlugins.Text += label71.Text;
                btnToggleEnable.ForeColor = Color.Green;
                btnToggleEnable.Text = "启用当前";
                lblPluginState.Text = "×";
                lblPluginState.ForeColor = Color.Crimson;
            }
        }

        private void button66_Click(object sender, EventArgs e)
        {
            cf.Write("plugin", "disabled", txtDisabledPlugins.Text);
        }

        private void button67_Click(object sender, EventArgs e)
        {
            txtDisabledPlugins.Text = cf.Read("plugin", "disabled");
        }

        private void chkUsePlugins_CheckedChanged(object sender, EventArgs e)
        {
            has_load_plugins = false;
        }
        int _cbTask_prev;
        private void cbTask_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cbTask.SelectedIndex == cbTask.Items.Count - 1)
            {
                TextBox _txtAddNewTask = new TextBox();
                this.grpSystem.Controls.Add(_txtAddNewTask);
                _txtAddNewTask.Location = cbTask.Location;
                _txtAddNewTask.Size = cbTask.Size;
                _txtAddNewTask.BringToFront();
                _txtAddNewTask.Focus();
                //cbTask.Visible = false;
                _txtAddNewTask.LostFocus += new System.EventHandler(this._txtAddNewTask_LostFocus);
                _txtAddNewTask.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this._txtAddNewTask_CheckEnter);
            }
            else
            {
                _cbTask_prev = cbTask.SelectedIndex;
                txtCondTasker.Text = cf.Read("tasker", cbTask.Items[cbTask.SelectedIndex].ToString());
                if (!txtCondTasker.Text.Contains("\"") && !txtCondTasker.Text.Contains("'"))
                    txtCondTasker.Text = "'" + txtCondTasker.Text + "'";
                label41.Text = "正在编辑任务:" + cbTask.Items[cbTask.SelectedIndex].ToString();
                button10.Text = "开始任务 " + cbTask.Items[cbTask.SelectedIndex].ToString();
            }

        }
        private void _txtAddNewTask_LostFocus(object sender, EventArgs e)
        {
            TextBox me = (TextBox)sender;
            if (me.Text == "")
            {
                cbTask.SelectedIndex = _cbTask_prev;
            }
            else if (cbTask.Items.IndexOf(me.Text) != -1)
            {
                MessageBox.Show("任务名\"" + me.Text + "\"已存在", "呵呵", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                cbTask.SelectedIndex = cbTask.Items.IndexOf(me.Text);
            }
            else
            {
                cf.Write("tasker", me.Text, "");
                cbTask.Items.Insert(cbTask.Items.Count - 1, me.Text);
                cbTask.SelectedIndex = cbTask.Items.Count - 2;
                if (MessageBox.Show("新任务\"" + me.Text + "\"已创建，是否现在编辑？\n你也可以稍后切换到任务选项卡编辑",
                    "呵呵", MessageBoxButtons.YesNo, MessageBoxIcon.Information) == DialogResult.Yes)
                {
                    tabControl1.SelectedIndex = 3;
                    //this.txtCondTasker_Leave(txtCondTasker, e);
                }
            }
            this.grpSystem.Controls.Remove(me);
            cbTask.Visible = true;
            me.Visible = false;
            me.Dispose();
        }
        private void _txtAddNewTask_CheckEnter(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == (char)13)
            {
                this.cbTask.Focus();
            }
        }
        private void notifyIcon1_MouseClick(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
                frmNormalize();

        }

        private void cboReservedName_SelectedIndexChanged(object sender, EventArgs e)
        {
            string[] _reserved_name = {"no_change", "abort", "letitgo"};
            if (cboReservedName.SelectedIndex != 0)
            {
                cboDeckList.Text = _reserved_name[cboReservedName.SelectedIndex - 1];
            }

        }

        private void chkAutoGreet_CheckedChanged(object sender, EventArgs e)
        {
            txtGreetWords.Enabled = chkAutoGreet.Checked;
        }

        private void txtReconnectGap_TextChanged(object sender, EventArgs e)
        {
            int x;
            if ((cboReconnectGapIndicator.SelectedIndex == 1 && !int.TryParse(txtReconnectGap.Text, out x)) ||
                (cboReconnectGapIndicator.SelectedIndex == 2 && !new Regex(@"\d+\:\d+").IsMatch(txtReconnectGap.Text)))
            {
                txtReconnectGap.ForeColor = Color.Red;
                txtReconnectGap.Font = new Font(textBox1.Font, FontStyle.Bold);
                toolTip1.SetToolTip(txtReconnectGap, "配置填写有误");
            }
            else
            {
                txtReconnectGap.ForeColor = Color.Black;
                txtReconnectGap.Font = new Font(textBox1.Font, FontStyle.Regular);
                toolTip1.SetToolTip(txtReconnectGap, "");
            }
        }

        private void cboReconnectGapIndicator_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cboReconnectGapIndicator.SelectedIndex == 0)
            {
                txtReconnectGap.Enabled = false;
                txtReconnectGap.Text = "0";
            }
            else
                txtReconnectGap.Enabled = true;
            txtReconnectGap_TextChanged(sender, e);

        }

        private void numFairyTimes_ValueChanged(object sender, EventArgs e)
        {
            if (numFairyTimes.Value == 0)
            {
                label23.Text = "无限刷妖精战";
                lblInfiniteWarning.Visible = true;
            }
            else
            {
                label23.Text = "刷妖精战" + numFairyTimes.Value + "次";
                lblInfiniteWarning.Visible = false;
            }
        }

        public static Encoding GetEncType(string fname)
        {
            byte[] b = File.ReadAllBytes(fname);
            return GetEncType(b);
        }

        public static Encoding GetEncType(byte[] bytes)
        {
            byte[] Unicode = new byte[] { 0xFF, 0xFE, 0x41 };
            byte[] UnicodeBIG = new byte[] { 0xFE, 0xFF, 0x00 };
            byte[] UTF8 = new byte[] { 0xEF, 0xBB, 0xBF }; //带BOM
            Encoding enc = Encoding.Default;
            if (IsUTF8Bytes(bytes) || (bytes[0] == 0xEF && bytes[1] == 0xBB && bytes[2] == 0xBF))
                enc = Encoding.UTF8;
            else if (bytes[0] == 0xFE && bytes[1] == 0xFF && bytes[2] == 0x00)
                enc = Encoding.BigEndianUnicode;
            else if (bytes[0] == 0xFF && bytes[1] == 0xFE && bytes[2] == 0x41)
                enc = Encoding.Unicode;
            return enc;

        }
        private static bool IsUTF8Bytes(byte[] data)
        {
            int cnt = 1; 
            byte cur;
            for (int i = 0; i < data.Length; i++)
            {
                cur = data[i];
                if (cnt == 1)
                {
                    if (cur >= 0x80)
                    {
                        while (((cur <<= 1) & 0x80) != 0)   cnt++;
                        if (cnt == 1 || cnt > 6)    return false;
                    }
                }
                else
                {
                    if ((cur & 0xC0) != 0x80)   return false;
                    cnt--;
                }
            }
            if (cnt > 1)
            {
                throw new Exception("这特么什么编码");
            }
            return true;
        }

        private void button81_Click(object sender, EventArgs e)
        {
            string dst = cboCfgFile.Text;
            byte[] b = File.ReadAllBytes(dst);
            if (b[0] == 0xef && b[1] == 0xbb && b[2] == 0xbf)
            {
                MessageBox.Show("BOM!");
                b = b.Skip(3).ToArray();
            }
            File.WriteAllText(dst, GetEncType(b).GetString(b), Encoding.Default);
            lblCfgEnc.Text = Encoding.Default.EncodingName;
            MessageBox.Show("搞定", "呵呵", MessageBoxButtons.OK, MessageBoxIcon.Information);
            lblEncWarning.Visible = false;
            lblEncWarningQuestion.Visible = false;
        }

        private void button82_Click(object sender, EventArgs e)
        {
            string dst = cboCfgFile.Text;
            byte[] b = File.ReadAllBytes(dst);

            StreamWriter sw = null;
            try
            {
                UTF8Encoding utf8 = new UTF8Encoding(false);
                using (sw = new StreamWriter(dst, false, utf8)) //no BOM
                {
                    sw.Write(GetEncType(b).GetString(b));
                }
            }catch{}
            lblCfgEnc.Text = Encoding.UTF8.EncodingName;
            MessageBox.Show("搞定", "呵呵",MessageBoxButtons.OK, MessageBoxIcon.Information);
            lblEncWarning.Visible = true;
            lblEncWarningQuestion.Visible = true;
        }

        private void linkLabel2_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (MessageBox.Show("不再显示此警告？", "呵呵", MessageBoxButtons.YesNo,
                MessageBoxIcon.Question) == DialogResult.Yes)
            {
                cf.Write("MAClientGUI", "no_enc_warning", "1");
                lblEncWarningQuestion.Visible = false;
                lblEncWarning.Visible = false;
            }
        }

        private void lblEncWarningQuestion_Click(object sender, EventArgs e)
        {
            tabControl1.SelectedIndex = 9;
        }

        private void numAutoRT_ValueChanged(object sender, EventArgs e)
        {
            var value = numAutoRT.Value.ToString().Split('.');
            numAutoRT.DecimalPlaces = value.Length == 2 ? value[1].Length : 0;
        }

        private void numAutoGT_ValueChanged(object sender, EventArgs e)
        {
            var value = numAutoGT.Value.ToString().Split('.');
            numAutoGT.DecimalPlaces = value.Length == 2 ? value[1].Length : 0;
        }

        private void button85_Click(object sender, EventArgs e)
        {
            txtOverrideVersion.Text = "";
            txtOverrideUA.Text = "";
            txtOverrideToken.Text = "";
        }

        private void button83_Click(object sender, EventArgs e)
        {
            saveOverride();
        }

        private void button84_Click(object sender, EventArgs e)
        {
            refreshOverride();
        }


    }
}

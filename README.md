MAClient是一个可以用来装B的百万亚瑟王客户端。支持台服、国服全区、韩服、日服和东南亚(新加坡)服。

## MAClient 网页版 for BAE
![chaojibang](http://ww1.sinaimg.cn/bmiddle/436919cbjw1ebx3ktnokkg200m00k741.gif)[Live Demo](http://111.206.45.12:30037/)

##步骤

###获得源代码

```shell
git clone https://github.com/fffonion/MAClient -b dev_bae
```
或者[下载zip包](https://github.com/fffonion/MAClient/archive/dev_bae.zip)

###部署

####添加部署
- 注册百度云引擎账号 http://developer.baidu.com/
- 进入[管理控制台](http://developer.baidu.com/console)
- 添加部署 -> 选择 **python-worker**；代码版本工具选择 **git**

####开通port服务
- 扩展服务 -> 添加新服务 -> port
- 申请通过后(现在好像不用申请了)进入配置
- 关联部署 选择刚才新建的引擎；端口号 填10007

####上传代码
- [管理控制台](http://developer.baidu.com/console)内按 **SVN/GIT地址** 下的 **点击复制**，复制git地址
- git remote add bae git地址
- git push bae dev_web_bae:master #注意，一定要push到远端的 **master分支**
- [管理控制台](http://developer.baidu.com/console)内点 快捷发布

**如果希望支持韩服**
- 请至[release](https://github.com/fffonion/MAClient/releases/tag/kr-crypt-ext)中下载自己系统的依赖库，并在git中提交后一并上传
- 未测试过兼容性


###访问
使用port服务中给的地址和端口号(不是自己填的10007)

###配置
- maclient_web_bot.py中的`maxconnected`可配置最大用户数量

###PS
* BAE python-worker 基础内存占用60M左右，单个用户增长内存1~2M，可按此选择执行单元配置
* 除maclient_web.py外的代码可热替换
* 应该没了

###License
[GPLv3](LICENSE)
部分代码来自[binux/libMA](https://github.com/binux/libMA)，[mengskysama/MAClient](https://github.com/mengskysama/MAClient)
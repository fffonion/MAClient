MAClient是一个可以用来装B的百万亚瑟王客户端。支持台服、国服全区、韩服、日服和东南亚(新加坡)服。

## MAClient 网页版
![chaojibang](http://ww1.sinaimg.cn/bmiddle/436919cbjw1ebx3ktnokkg200m00k741.gif)[Live Demo](http://ma.mengsky.net/)

##步骤

###获得源代码

```shell
git clone https://github.com/fffonion/MAClient -b dev_web
cd MAClient
```

###安装依赖模块

```shell
pip install ./requirements.txt
```

或手动安装
```
httplib2>=0.8
requests>=1.2.3
gevent>=1.0
gevent-websocket>=0.3.6
WebOb>=1.2.3
pycrypto>=2.6
recaptcha-client>=1.0.6
```

如果希望支持韩服
```
# 请至release(https://github.com/fffonion/MAClient/releases/tag/kr-crypt-ext)中下载自己系统的依赖库
unzip maclient_crypt_ext.*.zip
chmod +x maclient_crypt_ext.so
```

###访问http://[IP]:8000

###PS
* 单个用户增长内存1~2M
* 除maclient_web.py外的代码可热替换
* 应该没了

###License
[GPLv3](LICENSE)
部分代码来自[binux/libMA](https://github.com/binux/libMA)，[mengskysama/MAClient](https://github.com/mengskysama/MAClient)
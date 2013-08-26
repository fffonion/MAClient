#coding:utf-8
import httplib2
import re
import hashlib
import threading
import time
import urllib
class maRemote():
    class rpter(threading.Thread):
        def __init__(self,maRmt,name,statusloop,profileloop):
            threading.Thread.__init__(self,name=name)
            self.statusloop=statusloop
            self.profileloop=profileloop
            self.flag=1
            self.maRmt=maRmt
        def run(self):
            fc=self.profileloop/self.statusloop
            cnt=0
            while self.flag==1:
                time.sleep(self.statusloop)
                if self.maRmt.log_in:
                    self.maRmt.queryloop()
                    self.maRmt.lastquery=time.time()
                    if cnt==(fc-1) and self.maRmt.status==self.maRmt.STARTED:
                        self.maRmt.upload_profile()
                        self.maRmt.lastprofile=time.time()
                cnt=(cnt+1)%fc
    def __init__(self,name='',home='',statusloop=30,profileloop=180):
        #const
        self.STARTED,self.STOPPED,self.SLEEP=1,0,-1
        #val
        self.name=name
        self.home=home
        self.status=self.STARTED
        self.log_in=False
        self.ht=httplib2.Http()
        self.cookie=''
        self.iprofile={}
        self.rpt=self.rpter(self,name,statusloop,profileloop)
        self.rpt.setDaemon(True)
        self.rpt.start()
        self.lastquery=0
        self.lastprofile=0
        self.task=''
        
    def do(self,uri='',param='',method='GET'):
        if method=='GET':
            #print self.home+uri+'?'+param
            header={'Cookie':self.cookie}
            resp,ct=self.ht.request(self.home+uri+'?'+param,headers=header)
            if 'set-cookie' in resp:
                self.cookie=resp['set-cookie'].split(',')[-1].rstrip('path=/').strip()
            #print ct
            return ct
        elif method=='POST':
            pass
    '''def conn_status(self):
        #远程连接状况回报
        return self.lastquery,self.lastprofile'''
    def get_task(self):
        t=self.task
        self.task=''
        return t
    def login(self):
        self.log_in=True
        '''return True,msg'''
    def _set_status(self,s):
        self.status=s
    def set(self,sdict):
        for s in sdict:
            self.iprofile[s]=sdict[s]
    def queryloop(self):
        #to set status
        pass
    def upload_profile(self):
        #upload profile
        pass
    def fckfairy(self,fairy):
        #a f*cked fairy info (dict)
        pass

if __name__=='__main__':
    a=maMengsky('test','test')
    a.set({'ap':60,'bc':70})
    a.upload_profile()
    #a.start()
    #a.queryloop()
    #print a.status
    #if a.login():
    #    print 123
# -*- coding: utf-8 -*-
import cookielib
import urllib
import urllib2
import random
import time
from bs4 import BeautifulSoup

class Cookie:
    """
    获取或刷新cookie
    """
    def __init__(self, config):
        """
        构造函数
        """
        self.config = config
        self.cookie = ""
        #列表页总页数
        self.totalListPage = 0
        #初始化生存cookie
        self.refresh()
        
    def refresh(self):
        """
        清空现有cookie，重新设置搜索选项并生成cookie
        """
        cookiejar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        #Step 1: cookiejar记录ASP.NET_SessionId,LID,LID,SID_kns
        try:
            opener.open("http://epub.cnki.net/kns/brief/default_result.aspx")
        except:
            print "EXCEPTION(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):刷新Cookie时发生异常，休息" + str(self.config.get("urlopenExceptRetryInterval")) + "秒后重试"
            time.sleep(self.config.get("urlopenExceptRetryInterval"))
            opener.open("http://epub.cnki.net/kns/brief/default_result.aspx")
        #Step 2: 登录
        try:
            opener.open("http://epub.cnki.net/kns/Request/login.aspx?&td=" + str(int(time.time() * 1000)))
        except:
            print "EXCEPTION(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")：刷新Cookie时发生异常，休息" + str(self.config.get("urlopenExceptRetryInterval")) + "秒后重试"
            time.sleep(self.config.get("urlopenExceptRetryInterval"))
            opener.open("http://epub.cnki.net/kns/Request/login.aspx?&td=" + str(int(time.time() * 1000)))
        #Step 3: 设置搜索选项
        data = urllib.urlencode(self.config.get('search'))
        self.config.set("Cookie", self.generateCookieString(cookiejar), "headers")
        headers = self.config.get("headers")
        request = urllib2.Request("http://epub.cnki.net/KNS/request/SearchHandler.ashx", data, headers)
        try:
            opener.open(request)
        except:
            print "EXCEPTION(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")：刷新Cookie时发生异常，休息" + str(self.config.get("urlopenExceptRetryInterval")) + "秒后重试"
            time.sleep(self.config.get("urlopenExceptRetryInterval"))
            opener.open(request)
        additional = {
                      "RsPerPage":self.config.get("RecordsPerPage","list"),
                      "cnkiUserKey":self.generateCnkiUserKey()
                      }
        self.cookie = self.generateCookieString(cookiejar, additional)
        #Step 4:请求列表页第1页，设置检索参数
        data = urllib.urlencode(self.config.get('listPageOne'))
        self.config.set("Cookie", self.cookie, "headers")
        headers = self.config.get("headers")
        request = urllib2.Request("http://epub.cnki.net/kns/brief/brief.aspx", data, headers)
        try:
            response = opener.open(request)
        except:
            print "EXCEPTION(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")：刷新Cookie时发生异常，休息" + str(self.config.get("urlopenExceptRetryInterval")) + "秒后重试"
            time.sleep(self.config.get("urlopenExceptRetryInterval"))
            response = opener.open(request)
        #获取总页数
        soup = BeautifulSoup(response.read())
        if soup.find('span', {"class":"countPageMark"}):
            s = soup.find('span', {"class":"countPageMark"}).get_text()
            s = s.split("/")
            if len(s) >=2:
                self.totalListPage = int(s[1])
        return self.cookie

    
    def get(self):
        """
        获取已经存储的cookie
        """
        return self.cookie
    
    def getTotalListPage(self):
        """
        获取列表页总页数
        """
        return self.totalListPage
    
    def generateCnkiUserKey(self):
        """
        生成cookie中的cnkiUserKey值
        根据http://epub3.cnki.net/KRS//Scripts/Recommend.js内的SetNewGuid()函数改写
        """
        cnkiUserKey = ""
        for i in range(1, 33):
            # 生成0-15的整数，并将其转换为16进制形式
            n = random.randint(0, 15)
            # hex将整数转化为16进制形式"0xc"，取第三个字符
            n = hex(n)
            n = n[2]
            cnkiUserKey += n
            # 在第8，12，16，20个字符后面加上连字符(-)
            if i == 8 or i == 12 or i == 16 or i == 20:
                cnkiUserKey += "-"
        return cnkiUserKey
            
    def generateCookieString(self, cookiejar, additional = None):
        """
        根据cookiejar对象生成cookie字符串
        cookiejar:cookielib.CookieJar()对象
        additional:附加的用于生成cookie字符串的键值对字典
        """
        cookieString = ""
        for cookie in cookiejar:
            cookieString += cookie.name + "=" + cookie.value + "; "
        if additional:
            keys = additional.keys()
            for k in keys:
                cookieString += k + "=" + additional[k] + "; "
                
        if not cookieString == "":
            cookieString = cookieString[0:len(cookieString) - 2]
        return cookieString

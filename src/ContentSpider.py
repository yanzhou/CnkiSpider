# -*- coding: utf-8 -*-
import sys
import time
import urllib2
from bs4 import BeautifulSoup

class ContentSpider():
    """
    抓取内容页信息
    """
    
    def __init__(self, config, cookie):
        """
        构造函数
        config:Cofig对象
        cookie:Cookie对象
        """
        
        self.config = config
        self.cookie = cookie
        # 内容详情页url
        self.url = ""
        self.html = ""
        # 当前文章在列表页中的序号
        self.order = 1

    def fetchHtml(self, url, order):
        """
        获取内容详情页html
        url:列表页抓取的绝对路径
        order:当前文章在列表页中的序号
        """
        # 内容详情页url
        self.url = url
        self.order = order
        contentUrl = self.config.get("contentBaseUrl") + "?" + self.url
        # 设置头信息，Referer必填
        referer = self.config.get("listBaseUrl") + "?curpage=" + self.config.get("curpage", "list") + "&" + "RecordsPerPage=" + self.config.get("RecordsPerPage", "list") + "&" + "QueryID=" + self.config.get("QueryID", "list") + "&" + "ID=" + self.config.get("ID", "list") + "&" + "turnpage=" + self.config.get("turnpage", "list") + "&" + "tpagemode=" + self.config.get("tpagemode", "list") + "&" + "dbPrefix=" + self.config.get("dbPrefix", "list") + "&" + "Fields=" + self.config.get("Fields", "list") + "&" + "DisplayMode=" + self.config.get("DisplayMode", "list") + "&" + "PageName=" + self.config.get("PageName", "list") 
        self.config.set("Cookie", self.cookie.get(), "headers")
        self.config.set("Referer", referer, "headers")
        
        # 请求头配置
        headers = self.config.get("headers")
        request = urllib2.Request(contentUrl, "", headers)
        try:
            response = urllib2.urlopen(request)
        except:
            print "EXCEPTION(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):请求页面时发生异常，休息" + str(self.config.get("urlopenExceptRetryInterval")) + "秒后重试"
            time.sleep(self.config.get("urlopenExceptRetryInterval"))
            response = urllib2.urlopen(request)
        self.html = response.read()
        return self.html
    
    def getDetailInfo(self, html):
        """
        从详情页html中抽取信息
        """
        #检查html参数是否是验证码页面或者错出页面，并将内容页中的utf16标签去掉
        h = self.checkHtml(html)
        soup = BeautifulSoup(h)
        content = {}
#标题，已在ListSpider中检索出来
#         content["title"] = ""
#         if soup.find("span", {"id":"chTitle"}):
#             content["title"] = soup.find("span", {"id":"chTitle"}).get_text()
        #关键词
        content["keywords"] = ""
        if soup.find(id = "ChDivKeyWord"):
            keywords_list = soup.find("span", {"id":"ChDivKeyWord"}).find_all("a")
            for keyword in keywords_list:
                content["keywords"] += keyword.get_text() + "|"
        #摘要
        #TODO:摘要中如果含有换行符号则无法使用文本的方式一行存储，需要将摘要中的换行去掉再存储
        #content["abstract"] = ""
        #if soup.find("span", {"id":"ChDivSummary"}):
        #    content["abstract"] = soup.find("span", {"id":"ChDivSummary"}).get_text()
        #分类号
        #2013-11-28 13:16:55修复，如果有两个class="break"的ul则第一个是"【网络出版投稿人】XXX"
        content["categories"] = ""
        if soup.find_all("ul", {"class":"break"}):
            s = soup.find_all("ul", {"class":"break"})
            if len(s) > 1:
                s = s[1]
            else:
                s = s[0]
            if s.find('li'):
                s = s.find('li').get_text()
                s = s.replace("【分类号】".decode("utf8"), "")
                s = s.strip()              
                content["categories"] = s
                
        return content
    
    def save(self, info, handler):
        """
        保存抽取的文献信息
        使用Windows的\r\n作为换行符
        info:文献信息（字典类型）
        handler:打开的文件句柄
        sep:各个字段的分隔符
        """
        sep = self.config.get("fieldsSeperator")
        fields = self.config.get("fieldsOrder")
        s = ""
        for field in fields:
            s += info[field] + sep
        #TODO:容错，s必须长度大于XX
        s = s[0:len(s) - len(sep)] + self.config.get("lineSeperator")
        #s = info["order"] + sep + info["title"] + sep + info["time"] + sep + info["keywords"] + sep + info["categories"] + info + info["downloaded"] + sep + info["cited"] + sep + info["source"] + sep + info["authors"] + "\r\n"
        handler.write(s)
    
    
    def checkHtml(self, html):
        """
        检查内容页html是否是验证码输入页面或者错误页面或者cnki首页
        若是验证码页面或者错误页面则从新抓取并返回新的html页面
        """
        # 返回html
        h = html
        #内容页是utf16编码，需要进行如下处理，不可在fetchHtml()中处理，因为fetchHtml可能返回验证码页面
        h = h[0:139] + h[214:]
        soup = BeautifulSoup(h)
        # 如果要输入验证码则Refresh Cookie
        # 最大刷新次数
        refreshCookieTimes = self.config.get("refreshCookieTimes")
        # 刷新次数计数
        i = 1
        while(soup.find_all("input", {"id":"CheckCode"}) or soup.find_all(text="对不起，服务器上不存在此用户") or soup.html.head.title.string == "中国知网"):
            if i > refreshCookieTimes:
                print "ERROR(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):刷新" + str(refreshCookieTimes) + "次仍无法继续抓取内容详情页"
                print "###############STOP###############"
                sys.exit(0)
            print "TRYING(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):休息" + str(self.config.get("refreshCookieInterval")) + "秒"
            time.sleep(self.config.get("refreshCookieInterval"))
            print "WARNING(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")：抓取第" + str(self.order) + "篇文献时需要刷新Cookie"
            print "TRYING(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")：第" + str(i) + "次刷新Cookie"
            self.cookie.refresh()
            print "TRYING(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):重新抓取第" + str(self.order) + "篇文献"
            h = self.fetchHtml(self.url, self.order)
            h = h[0:139] + h[214:]
            soup = BeautifulSoup(h)
            i = i + 1
        return h

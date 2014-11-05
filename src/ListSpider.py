# -*- coding: utf-8 -*-
import sys
import time
import codecs
import urllib
import urllib2
import re
from bs4 import BeautifulSoup

class ListSpider:
    """
    抓取处理列表页数据
    """
    
    def __init__(self, config, cookie):
        """
        构造函数
        config:Cofig对象
        cookie:Cookie对象
        """
        
        self.config = config
        self.cookie = cookie
        # 列表页html
        self.html = ""
    
    def fetchHtml(self, page):
        """
        获取列表页html
        page：页码
        """
        self.page = str(page)
        self.config.set("Cookie", self.cookie.get(), "headers")
        self.config.set("curpage", self.page, "list")
        # 请求头配置
        headers = self.config.get("headers")
        # bug:urllib2.Request的第一个参数必须是listBaseUrl加上查询字符串，并且第二个参数是查询字符串
        url = self.config.get("listBaseUrl") + "?curpage=" + self.config.get("curpage", "list") + "&" + "RecordsPerPage=" + self.config.get("RecordsPerPage", "list") + "&" + "QueryID=" + self.config.get("QueryID", "list") + "&" + "ID=" + self.config.get("ID", "list") + "&" + "turnpage=" + self.config.get("turnpage", "list") + "&" + "tpagemode=" + self.config.get("tpagemode", "list") + "&" + "dbPrefix=" + self.config.get("dbPrefix", "list") + "&" + "Fields=" + self.config.get("Fields", "list") + "&" + "DisplayMode=" + self.config.get("DisplayMode", "list") + "&" + "PageName=" + self.config.get("PageName", "list") 
        data = urllib.urlencode(self.config.get("list"))
        request = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(request)
        except:
            print "EXCEPTION(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):请求页面时发生异常，休息" + str(self.config.get("urlopenExceptRetryInterval")) + "秒后重试"
            time.sleep(self.config.get("urlopenExceptRetryInterval"))
            response = urllib2.urlopen(request)
        self.html = response.read()
        return self.html
    
    def getArticles(self, html):
        """
        获取文献列表
        html:列表页html
        """
        #检查页面是否是验证码页面或者错误页面
        soup = BeautifulSoup(self.checkHtml(html))
        contents = []
        #抽取文章列表
        #如果列表页有文章，抽取文章url和相关字段返回
        if soup.find('table', {"class":"GridTableContent"}):
            articles = soup.find('table', {"class":"GridTableContent"}).find_all('tr')
            if articles:
                #循环抓取内容页,第一行是表头，不使用
                for index in range(1, len(articles)):
                    #每篇文章的基本信息在不同的<td>中，第一个td是序号
                    article = articles[index].find_all('td')
                    content = {}

                    #文章序号
                    content["order"] = article[0].get_text()

                    #文章链接
                    if article[1].find('a') and article[1].find('a').get('href'):
                        content["url"] = article[1].find('a').get('href')
                    #若文章链接不存在，则该篇文章不抓取
                    else:
                        print "WARNING(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):第" + str(content["order"]) + "篇文章没有链接，跳过，继续下一篇"
                        continue
                    #标题，从js中检索
                    if article[1].find('script'):
                        s = article[1].find('script').string
                        s = s.replace("document.write(ReplaceChar1(ReplaceChar(ReplaceJiankuohao('", "")
                        s = s.replace("'))));","")
                        s = s.replace("<font class=Mark>","")
                        s = s.replace("</font>","")
                        content["title"] = s
                        
                    #每个作者位于一个<a>标签内
                    content["authors"] = ""
                    if article[2].find_all('a'):
                        authors = article[2].find_all('a')
                        for author in authors:
                            #结尾多了一个分号
                            content["authors"] += author.get_text() +";"

                    #来源期刊或机构
                    content["source"] = ""
                    if article[3].find("script"):
                        s = article[3].find("script").get_text()
                        k = re.findall(u"[\u4e00-\u9fa5]+\(?[\u4e00-\u9fa5]+\)?",s)
                        if k:
                            content["source"] = k[0]

                    #发表时间
                    content["time"] = ""
                    s = article[4].get_text()
                    s = s.replace("\r\n","")
                    s = s.strip()
                    content["time"] = s
                    
                    #来源数据库，如期刊，硕士，博士等
                    content["db"] = ""
                    s = article[5].get_text()
                    s = s.replace("\r\n","")
                    s = s.strip()
                    content["db"] = s
        
                    #被引次数
                    content["cited"] = "0"
                    if article[6].find('a'):
                        content["cited"] = article[6].find('a').get_text()

                    #下载次数
                    content["downloaded"] = "0"
                    if article[7].find("span", {"class" : "downloadCount"}):
                        content["downloaded"] = article[7].find("span", {"class" : "downloadCount"}).get_text()
                    #存如contents列表里
                    contents.append(content)
        return contents
    
    def saveHtml(self, html):
        """
        保存列表页html页面
        """
        #检查页面是否是验证码页面或者错误页面
        html = self.checkHtml(html)
        path = self.config.get("outputListPagesDir") + self.page + ".txt"
        content = html.decode('utf-8')
        f = codecs.open(path,'w', encoding='utf-8')
        f.write(content)
        f.close()
        
    def checkHtml(self, html):
        """
        检查抓取的html页面是否是验证码页面或者session过期提示页面或者cnki首页
        返回html
        """
        #返回html
        h = html
        soup = BeautifulSoup(h)
        # 如果要输入验证码则Refresh Cookie
        # 最大刷新次数
        refreshCookieTimes = self.config.get("refreshCookieTimes")
        # 刷新次数计数
        i = 1
        while(soup.find_all("input", {"id":"CheckCode"}) or soup.find_all(text = "对不起，服务器上不存在此用户") or soup.html.head.title.string == "中国知网"):
            if i > refreshCookieTimes:
                print "ERROR(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):刷新" + str(refreshCookieTimes) + "次仍无法继续抓取列表页"
                print "###############STOP###############"
                sys.exit(0)
            print "TRYING(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):休息" + str(self.config.get("refreshCookieInterval")) + "秒"
            time.sleep(self.config.get("refreshCookieInterval"))
            print "WARNING(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")：抓取列表页第" + str(self.page) + "页时需要刷新Cookie"
            print "TRYING(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")：第" + str(i) + "次刷新Cookie"
            self.cookie.refresh()
            print "TRYING(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):重新抓取第" + str(self.page) + "页列表页"
            h = self.fetchHtml(self.page)
            soup = BeautifulSoup(h)
            i = i + 1
        return h

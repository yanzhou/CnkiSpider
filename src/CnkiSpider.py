# -*- coding: utf-8 -*-
"""
抓取CNKI的主程序
默认检索所有学科的"文献"类型的文章（包含期刊，硕士论文，博士论文等）
注意:1.在使用数据前请浏览以确认所有字段格式无误，如某些文献的作者字段可能会多出换行符未处理掉，将导致转换成xls文件时多出空白行
    2.不含关键字字段和分类字段的文献很可能是内容页没有成功抓取的，这个bug以后改进
    3.摘要的内容代码里面已成功抽取，若要添加需要修改ContentSpider.py(69-71),Config.py(29),CnkiSpider.py(70)
    4.中断后从断点页面继续爬取请设置startPage参数
    5.数据文件名名称格式为："data-keyword-年月日时分秒.txt",如"data-新媒体-20131128141415.txt"中断后继续爬取会重新根据当前时间生成新的文件，最后将多个文件合并即可
TODO:1.网络超时控制（暂时解决办法：抓取中断后设置startPage为中断页重新抓取）
     2.根据内容页url抓取内容页会被跳转到CNKI首页从而导致内容页无法抓取，即关键字和分类号字段缺失
     3.设置配置文本文件，配置项写如其中而不必修改该文件来设置配置项
     4.智能评估抓取多少页后需要休息多长时间才能避免抓取过快在内容页时被从定向到CNKI首页而无法获取内容详情页信息
"""
import codecs
import time
from Config import Config
from Cookie import Cookie
from ListSpider import ListSpider
from ContentSpider import ContentSpider

"""
设置部分
更多自定义设置请参照Config.py文件定义
"""
config = Config()
#设置搜索关键词
keyword = "新媒体"
config.set("txt_1_value1", keyword, "search")
#设置关键字检索范围："FT$%=|"(全文);"SU$%=|" selected="true"(主题);"TI$%=|"(篇名);"KY$=|"(关键词);"AU$=|"(作者);"AF$%"(单位);"LY"(刊名);"SN$=|??"(ISSN);"CN$=|??"(CN);"FU"(基金);"AB$%=|"(摘要);"RF$%=|"(参考文献);"CLC$=|??"(中图分类号);
x = "FT$%=|"
config.set("txt_1_sel", x, "search")
#设置检索匹配方式,"%"(模糊查询),"="(精确查询)
match = "%"
config.set("txt_1_special1", match, "search")
#设置检索学科，默认检索所有学科（*）。各学科代码参见 ./doc/categories.json文件
discipline = "*"
config.set("NaviCode", discipline, "search")
#设置字段分隔符
fieldsSep = "###"
config.set("fieldsSeperator", fieldsSep)
#设置行分隔符，若数据文件主要在Windows下使用，则设置为\r\n,若Linux下则设置为\r或\r\n
lineSep = "\r\n"
config.set("lineSeperator", lineSep)
#每抓取restEvery页列表页后休息restPeriod秒
restEvery = 20
config.set("restEvery", restEvery)
restPeriod = 60
config.set("restPeriod", restPeriod)

#起始列表页，用于中断后接着爬取
startPage = 1

cookie = Cookie(config)
listspider = ListSpider(config, cookie)
contentspider = ContentSpider(config, cookie)

#打开存储内容的文件
fileName = config.get("outputPath") + "data-" + config.get("txt_1_value1", "search").decode("utf8") + "-" + time.strftime("%Y%m%d%H%M%S") + ".txt"
handler = codecs.open(fileName,'a', encoding='utf-8')
#字段分隔符
sep = config.get("fieldsSeperator")
#数据表头
header = ""
fields = config.get("fieldsOrder")
for field in fields:
    header += field + sep
header = header[0:len(header) - len(sep)] + config.get("lineSeperator")
handler.write(header)

# 获取列表页总页数
totalListPages = cookie.getTotalListPage()
print "################START(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")列表页总数:" +str(totalListPages) + "################"
for i in range(startPage, totalListPages + 1):
    print "LIST:获取列表页:" + str(i) + "/" + str(totalListPages)
    #每抓取config["restEvery"]页列表页后休息config["restPeriod"]秒
    if i % config.get("restEvery") == 0:
        print "REST(" + time.strftime("%Y-%m-%d %H:%M:%S") + "):又抓取了" + str(config.get("restEvery")) + "页了，休息" + str(config.get("restPeriod")) + "秒吧～"
        time.sleep(config.get("restPeriod"))
        
    articlesList = listspider.getArticles(listspider.fetchHtml(i))
    for article in articlesList:
        print "----CONTENT:获取第" + str(article["order"]) + "篇文章"
        contentHtml = contentspider.fetchHtml(article["url"], int(article["order"]))
        content = contentspider.getDetailInfo(contentHtml)
        #从article和content抽取信息存储
        save = {}
        save["order"] = article["order"]
        save["authors"] = article["authors"]
        save["source"] = article["source"]
        save["time"] = article["time"]
        save["db"] = article["db"]
        save["cited"] = article["cited"]
        save["downloaded"] = article["downloaded"]
        save["title"] = article["title"]
        save["keywords"] = content["keywords"]
        save["categories"] = content["categories"]
        #save["abstract"] = content["abstract"]
        #存储之前将所有字符过滤一遍，去掉换行符,去掉两端的空白
        for k in save:
            save[k] = save[k].replace("\r\n", "")
            save[k] = save[k].strip()
        contentspider.save(save, handler)
handler.close()
print "################END(" + time.strftime("%Y-%m-%d %H:%M:%S") + ")################"
        

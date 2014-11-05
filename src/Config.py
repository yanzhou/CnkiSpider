# -*- coding: utf-8 -*-
import time

class Config:
    """
    配置类
    """
    
    def __init__(self):
        """
        构造函数
        设置默认配置项
        """
        self.config = {}
        """
        系统配置
        """
        # 保存抓取数据的文件路径，默认为当前文件夹下data.txt文件
        self.config["outputPath"] = "../data/"
        #列表页保存路径，需要手动创建好文件夹
        self.config["outputListPagesDir"] = "../data/ListPages/"
        # 列表页Base URL，用于加上其他参数构造列表页URL
        self.config["listBaseUrl"] = "http://epub.cnki.net/kns/brief/brief.aspx"
        # 内容页Base URL，用于加上其他参数构造内容页URL
        self.config["contentBaseUrl"] = "http://epub.cnki.net/kns/detail/detail.aspx"
        # 输出各个字段之间的分割符
        self.config["fieldsSeperator"] = "###"
        #输出的各个字段及顺序
        self.config["fieldsOrder"] = ["order","title","time","keywords","categories","downloaded","cited","source","authors","db"]
        #换行符号
        self.config["lineSeperator"] = "\r\n"
        #需要输入验证码时刷新Cookie的次数
        self.config["refreshCookieTimes"] = 3
        #刷新Cookie时间间隔
        self.config["refreshCookieInterval"] = 5
        #每抓取config["restEvery"]个页面列表页后休息config["restPeriod"]秒
        self.config["restEvery"] = 20
        self.config["restPeriod"] = 60
        #urlopen发生异常后重试时间间隔
        self.config["urlopenExceptRetryInterval"] = 120
        """
        请求头配置
        """
        self.config["headers"] = {}
        self.config["headers"]["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
        
        """
        搜索表单配置
        配置项可选参数：
        ConfigFile:      "SCDBINDEX.xml"
        dbCatalog:  "中国学术文献网络出版总库"
        dbPrefix(文献类型):  "SCDB"(文献);"CJFQ"(期刊);"CDMD"(博硕士);"CIPD"(会议);"CCND"(报纸);
                                "WWJD"(外文文献);"CYFD"(年鉴);"CRPD"(百科);"CRDD"(词典);
                                "CSYD"(统计数据);"SCOD"(专利);"CISD"(标准);"IMAGE"(图片);"SNAD"(成果);
                                "CIDX"(指数);"CLKD"(法律);"GXDB_SECTION"(古籍);"CRLD"(引文);"CRMD"(手册)
        NaviCode(文献分类编码):"*"(all,default)参见categories.json，如"A001"表示"自然科学理论与方法"
        PageName:保持默认值"ASP.brief_default_result_aspx"，不许要修改
        __(当前时间字符串):形式为"Tue Nov 26 2013 23:02:44 GMT+0800 (CST)"
        action:留空
        db_opt(可选数据库,一般跟DbPrefix相同，若DbPrefix为SCDB则该值可以是多个dbPrefix可选值用逗号分隔的字符串):如"CJFQ,CJFN,CDFD"
        his():"0"
        parentdb():"SCDB"
        txt_1_sel(关键字搜索范围):"FT$%=|"(全文);"SU$%=|" selected="true"(主题);"TI$%=|"(篇名);
                                "KY$=|"(关键词);"AU$=|"(作者);"AF$%"(单位);"LY"(刊名);"SN$=|??"(ISSN);
                                "CN$=|??"(CN);"FU"(基金);"AB$%=|"(摘要);"RF$%=|"(参考文献);"CLC$=|??"(中图分类号);
        txt_1_special1(模糊或者精确查询):"%"(模糊查询),"="(精确查询)
        txt_1_value1(搜索关键词):如"自媒体"
        ua(子查询检索):保持默认值"1.11"不要修改，"1.11"(直接检索),"1.12"(在有侧栏中检索),"1.16"(在结果中检索)
        
        DisplayMode(列表页显示模式):"listmode"(列表模式)，"custommode"(摘要模式)
        S:  1
        
        dbPrefix(文献类型):  "SCDB"(文献);"CJFQ"(期刊);"CDMD"(博硕士);"CIPD"(会议);"CCND"(报纸);
                                "WWJD"(外文文献);"CYFD"(年鉴);"CRPD"(百科);"CRDD"(词典);
                                "CSYD"(统计数据);"SCOD"(专利);"CISD"(标准);"IMAGE"(图片);"SNAD"(成果);
                                "CIDX"(指数);"CLKD"(法律);"GXDB_SECTION"(古籍);"CRLD"(引文);"CRMD"(手册)
        keyValue(要搜索的关键词):如"自媒体"
        pagename:"ASP.brief_default_result_aspx"
        research:"off"
        t(系统时间毫秒数):int(time.time() * 1000)
        """
        self.config["search"] = {}
        self.config["search"]["ConfigFile"] = "SCDBINDEX.xml"
        self.config["search"]["dbCatalog"] = "中国学术文献网络出版总库"
        self.config["search"]["dbPrefix"] = "SCDB"
        self.config["search"]["NaviCode"] = "*"
        self.config["search"]["PageName"] = "ASP.brief_default_result_aspx"
        self.config["search"]["__"] = time.strftime("%a %b %d %Y %H:%M:%S GMT+0800 (CST)")
        self.config["search"]["action"] = ""
        self.config["search"]["db_opt"] = "CJFQ,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,CCJD,HBRD"
        self.config["search"]["his"] = "0"
        self.config["search"]["parentdb"] = "SCDB"
        self.config["search"]["txt_1_sel"] = "FT$%=|"
        self.config["search"]["txt_1_special1"] = "%"
        self.config["search"]["txt_1_value1"] = "新媒体"
        self.config["search"]["ua"] = "1.11"
        
        """
        重要
        生成cookie的时候需要爬取列表页第一页，发送检索选项
        爬取第一个列表页的时候参数不同
        """
        self.config["listPageOne"] = {}
        self.config["listPageOne"]["ConfigFile"] = self.config["search"]["ConfigFile"]
        self.config["listPageOne"]["S"] = "1"
        self.config["listPageOne"]["dbCatalog"] = self.config["search"]["dbCatalog"]
        self.config["listPageOne"]["dbPrefix"] = self.config["search"]["dbPrefix"]
        self.config["listPageOne"]["keyValue"] = self.config["search"]["txt_1_value1"]
        self.config["listPageOne"]["pagename"] = self.config["search"]["PageName"]
        self.config["listPageOne"]["research"] = "off"
        self.config["listPageOne"]["t"] = int(time.time() * 1000)
        
        """
        爬取列表页和内容页所需要的参数
        保持默认即可
        """
        self.config["list"] = {}
        self.config["list"]["DisplayMode"] = "listmode"
        self.config["list"]["Fields"] = ""
        self.config["list"]["ID"] = ""
        self.config["list"]["PageName"] = "ASP.brief_default_result_aspx"
        self.config["list"]["QueryID"] = "0"
        self.config["list"]["RecordsPerPage"] = "20"
        self.config["list"]["dbPrefix"] = "SCDB"
        self.config["list"]["sKuaKuID"] = "0"
        self.config["list"]["tpagemode"] = "L"
        self.config["list"]["turnpage"] = "1"
        self.config["list"]["curpage"] = "1"
        
    def get(self, key, parent=None):
        """
        获取配置
        key:配置项键名
        parent:上级键名，search，list或None
        """
        if key and key in self.config.keys():
            return self.config[key]
        elif parent in ["list", "search", "headers", "listPageOne"]:
            return self.config[parent][key]
        else:
            return None
    
    def set(self, key, val, parent=None):
        """
        设置配置项
        key:键名
        val:键值
        parent:上级键名，search，list或None
        """
        if key and val and key in self.config.keys():
            self.config[key] = val
        elif key and val and parent in ["list", "search", "headers", "listPageOne"]:
            self.config[parent][key] = val

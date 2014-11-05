1. 在src/CnkiSpider.py设置检索条件

2. 执行src/CnkiSpider.py抓取数据

3. 抓取数据存储在/data目录下，文件名格式为"data-keyword-年月日时分秒.txt.txt"，如"data-新媒体-20131128224556.txt"

4. 每个数据文件的第一行为字段名称

5. 每次运行都根据当前时间生成新的数据文件

6. 如果抓取过程中断，可以在src/CnkiSpider.py中设置startPage为中断时的页码，并重新运行src/CnkiSpider.py从中断的页面继续抓取，最后将各个数据文件合并

7. 生成的文本文件直接修改后缀名为.csv然后用LibreOffice打开并在LibreOffice中设置字段分隔符为src/CnkiSpider.py中变量fieldsSep设置的字符串

8. Windows下打开Excel 2013,然后【打开】->【浏览】->选择文件（文件名后下拉框选择“文本文件”），出现文本导入向导，设置“文件原始格式”为Unicode（UTF-8)，下一步，设置“分隔符号”

9. 由若要使用文本编辑器打开数据文件，建议使用Notepad++打开。Windows自带的记事本打开大文件会卡死。Notepad++可以自动识别编码格式，防止乱码。

10. 如果数据文件中从某部分开始大量出现关键词字段和分类号字段为空的情况，则将src/CnkiSpider.py中restEvery变量调小，restPeriod变量调大后重试。

## diff Windows version and Linux version

CnkiSpider.py        print "----CONTENT:获取第" + str(article["order"]) + "篇文章"

ContentSpider.py     s = s.replace("【分类号】".decode("utf8"), "")
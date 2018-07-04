# -*- coding=utf-8 -*-
import sys #系统曾
import csv #csv文件操作
import codecs #编码问题
import re
#获取数据处理用到的拓展
import requests 
import urllib.request

# from tld import get_tld

from lxml import etree
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.request import Request

#程序运行常量配置
HTTP_HEADERS = { 'Accept': '*/*','Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
HTTP_TIMEOUT = 15

# xpath 定义
BAIDU_COUNT = '//*[@id="container"]/div[2]/div/div[2]/span'
 

# class MyRedirectHandler(urllib.request.HTTPRedirectHandler):
#     def http_error_302(self, req, fp, code, msg, hdrs):
#         return fp


#操作csv的方法
class SetCsv:
    '''将百度爬取的数据写入csv'''
    def __init__(self, fileName):
        '''初始化文件'''
        self.filename = fileName + '.csv'
        self.csvfile = codecs.open(self.filename, 'w+', 'utf_8_sig')
        self.setfile = csv.writer(self.csvfile)
    def setParams(self,data):
        '''写入文件'''
        self.setfile.writerow(data)
    def closeFile(self):
        '''关闭文件流'''
        self.csvfile.close()

class GetBaidu:
    """docstring for GetBaidu"""
    def __init__(self, serUrl): 
        self.serUrl = serUrl

    def getFirst(self):
        """获取聚合结果"""
        r = requests.get(self.serUrl,headers=HTTP_HEADERS,timeout=HTTP_TIMEOUT)
        if r.status_code != 200:
            file.setParams(("本次请求失败",r.status_code,self.serUrl))           
        html = etree.HTML(r.text)
        return html
    def getList(self):
        """开始请求并将结果编入list返回"""
        listHtml = self.getFirst()
        resultList = []
        retList = listHtml.xpath('//body/div/div/div/div/div/h3/a')
        for a in retList:
            title = a.xpath('string(.)').strip()
            baiduHashUrl = a.xpath('string(@href)').strip()
            
            # req = Request(baiduHashUrl)
            # # 模拟一个浏览器访问百度, 不然不会重写到 https.
            # req.add_header('User-Agent','Mozilla/5.0 (X11 Linux x86_64 rv:47.0) Gecko/20100101 Firefox/47.0')
            # res = opener.open(req).getheaders()
            # for resOne in res:
            #     if resOne[0] == "Location":
            #         realUrl = resOne[1]
            #         break
            # print(realUrl)
            # if realUrl.endswith('/'):
            try:
                webUrlGet = requests.get(baiduHashUrl,headers=HTTP_HEADERS,timeout=HTTP_TIMEOUT)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
                continue

            if webUrlGet.status_code != 200:
                print(title,webUrlGet.status_code,baiduHashUrl) 
                continue
            
        
            oneList = [0,1,2,3]
            oneList[0] = title
            oneList[1] = webUrlGet.url

            self.serUrl = 'http://www.baidu.com/s?ie=utf-8&wd=site:'+ urlparse(webUrlGet.url).netloc
            sitehtml = self.getFirst()
            # print(self.serUrl);
            getSite = sitehtml.xpath('//*[@id="content_left"]/div[1]/div/p[1]/b/text()')
            if len(getSite):
                getSite = re.sub("\D", "", getSite[0])
            else:
                try:
                    getSite = sitehtml.xpath('//*[@id="1"]/div/div[1]/div/p[3]/span/b/text()')[0]
                except Exception as e:
                    getSite = self.serUrl + "未取到 site"
 

            oneList[2] = getSite

            webUrlGetHtml = etree.HTML(webUrlGet.text)
            # 验证sdk是否完整
            try:
                tidT = webUrlGetHtml.xpath("/html/head/title/text()") 
                tidD = webUrlGetHtml.xpath("/html/head/meta[@name='description']/@content")
                tidK = webUrlGetHtml.xpath("/html/head/meta[@name='keywords']/@content") 
                if tidT[0] and tidD[0] and tidK[0]:
                    oneList[3] = "完整"
                else:
                    oneList[3] = "不完整"
            except IndexError:
                oneList[3] = "不完整"
            except TypeError:
                oneList[3] = "不完整"              
            csone = tuple(oneList)
            file.setParams(csone);
        


#开始百度的搜索
reqQuestion = input("Search:")
reqUrl = 'http://www.baidu.com/s?ie=utf-8&wd=' + reqQuestion
resFirstHtml = GetBaidu(reqUrl).getFirst()
#展现页面收录统计
showGetCount = resFirstHtml.xpath(BAIDU_COUNT+'/text()')
print(format(showGetCount[0]))

resPage = int(input("unit:"))


# exit()

# opener = urllib.request.build_opener(MyRedirectHandler())
file = SetCsv(reqQuestion) 

nowPage = 0
while nowPage < resPage:
    nowPage += 10
    sys.stdout.write('正在筛选数据中 {0}/{1} 如果想停止，请按键 Ctrl + C \r'.format(nowPage , resPage))
    sys.stdout.flush()
    wgetUrl = reqUrl+'&pn='+str(nowPage)
    biduList = GetBaidu(wgetUrl).getList() 
file.closeFile()
print('获取数据 {0}/{1} 完成 \r'.format(resPage , resPage))
 
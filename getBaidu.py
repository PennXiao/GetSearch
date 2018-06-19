# coding=UTF-8
#获取数据用到的拓展
import requests 
from lxml import etree
#写入文件用到的拓展
import csv
import codecs

class SetCsv:
    '''将百度爬取的数据写入csv'''

    def __init__(self, fileName):
        '''初始化文件'''
        self.filename = fileName + '.csv'
        self.csvfile = codecs.open(self.filename, 'w+', 'utf_8_sig')
        self.setfile = csv.writer(self.csvfile)

    def setParams(self,data):
        '''写入单行文件'''
        self.setfile.writerow(data)

    def closeFile(self):
        '''关闭文件流'''
        self.csvfile.close()

#搜索的问题
reqQuestion = '凤凰'


#百度的搜索规则
reqUrl =  'http://www.baidu.com/s?ie=utf-8&wd=' + reqQuestion
reqPn = 0 #百度页面规则&pn=页面搜索条件


file = SetCsv(reqQuestion)
file.setParams(("本次请求的url ",reqUrl))

r = requests.get(reqUrl)
if r.status_code != 200:
    file.setParams(("本次请求的状态是",r.status_code))
    exit;

html = etree.HTML(r.text)

getCount = html.xpath('//body/div/div/div/div/div/div/span[@class="nums_text"]/text()')
print(format(getCount))

retList = html.xpath('//body/div/div/div/div/div/h3/a')
for a in retList:
    url = a.xpath('string(@href)').strip()
    title = a.xpath('string(.)').strip()
    file.setParams((title,url))


file.closeFile()

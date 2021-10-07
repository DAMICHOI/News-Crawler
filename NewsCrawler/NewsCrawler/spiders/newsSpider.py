# -*- coding: utf-8 -*-

import scrapy
from NewsCrawler.items import NewscrawlerItem
from datetime import datetime
import re
import math
import requests
from bs4 import BeautifulSoup

# firebase 연동 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('dev-11-abf32-firebase-adminsdk-mx60d-99f59c14c1.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


class NewsUrlSpider(scrapy.Spider):
    name = "newsCrawler"
    date1 = datetime.now().strftime('%Y.%m.%d')
    date2 = datetime.now().strftime('%Y%m%d')
    def start_requests(self):
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=0&photo=0&field=0&pd=3&ds={1}&de={1}&cluster_rank=1&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{2}to{2},a:all&start={3}'
        # companies = ['카카오', '네이버', '삼성전자', '현대자동차', '셀트리온', 'SK 이노베이션', 'LG 에너지 솔루션', '라인', '쿠팡', '배달의 민족']
        companies =['카카오']
        

        for company in companies:
            
            for page in range(1, 12, 10):
                yield scrapy.Request(url.format(company, self.date1,self.date2, page), self.parse_url)    


    def parse_url(self, response):
        for li in response.xpath('//*[@class="bx"]'):
            item = NewscrawlerItem()
            item['journal'] =  li.xpath('div[1]/div/div[1]/div[2]/a[1]/text()').extract()[0]  # 신문사
            item['company'] = response.xpath('//*[@id="nx_query"]/@value').extract()[0]   # 회사
            item['title'] = li.xpath('div[1]/div/a/@title').extract()[0] # 제목
            item['date'] = self.date1 # 작성일
            item['newsUrl'] = li.xpath('div[1]/div/a/@href').extract()[0]
            item['photoUrl'] = li.xpath('div[1]/a/img/@src').extract()
            
            db.collection(u'신문기사').document().set(item)
       
            yield item
    
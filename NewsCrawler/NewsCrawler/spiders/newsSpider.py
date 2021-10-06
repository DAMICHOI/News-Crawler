# -*- coding: utf-8 -*-

import scrapy
from NewsCrawler.items import NewscrawlerItem
from datetime import datetime
import re
import math
import requests
from bs4 import BeautifulSoup

#firebase 연동 
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# cred = credentials.Certificate('practice-7ee66-firebase-adminsdk-3aa3r-680925e0d5.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()


# 다음 뉴스 최대 페이지 구하는 메소드 
# def get_maxpage(url):
#         response = requests.get(url)
#         html = response.text
#         soup = BeautifulSoup(html, 'html.parser')
#         cnt = soup.find('span',{'id' : 'resultCntArea'}).get_text()
#         total_count = re.sub('[^0-9]', '', cnt.split('/')[1])
#         total_pages = math.ceil(int(total_count) / 10)
#         return total_pages


class NewsUrlSpider(scrapy.Spider):
    name = "newsCrawler"
    date1 = datetime.now().strftime('%Y.%m.%d')
    date2 = datetime.now().strftime('%Y%m%d')
    def start_requests(self):
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=0&photo=0&field=0&pd=3&ds={1}&de={1}&cluster_rank=102&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{2}to{2},a:all&start={3}'
        # companies = ['카카오', '네이버', '삼성전자', '현대자동차', '셀트리온', 'SK 이노베이션', 'LG 에너지 솔루션', '라인', '쿠팡', '배달의 민족']
        companies =['카카오']
        

        for company in companies:
            # maxpage = get_maxpage(url.format(company, self.date, 1))
        
            # for page in range(1, maxpage + 1):
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
            item['photoUrl'] = li.xpath('div[1]/a/img/@src').extract()[0]
            
            #db.collection(u'신문기사').document(item['company']).collection(self.date2).set(item)
            print('*' * 100)
            print(item['title'])
            print(item['company'])
            print(item['journal'])
            print(item['date'])
            print(item['newsUrl'])
            print(item['photoUrl'])
            print(response)
            yield item

    # def start_requests(self):
    #     press = ['024'] # 024: 경제
    #     pageNum = 2
    #     date = [20210905]
    #
    #     for cp in press:
    #         for i in range(1, pageNum, 1):
    #             yield scrapy.Request("http://www.etnews.com/news/section.html?id1=02&id2={0}&page={1}".format(cp, i),
    #                                  self.parse_url)
    #
    # def parse_url(self, response):
    #     for sel in response.xpath('/html/body/div/main/div/ul[@class="list_news"]/li/dl[@class="clearfix"]'):
    #
    #         yield scrapy.Request("http:"+sel.xpath('dt/a/@href').extract()[0],
    #                              callback=self.parse_news)
    #
    # def parse_news(self, response):
    #     item = NewscrawlerItem()
    #
    #     item['source'] = '전자신문'
    #     item['category'] = '경제'
    #     item['title'] = response.xpath('/html/head/meta[20]/@content').extract()[0]
    #     item['date'] = response.xpath('/html/head/meta[contains(@property, "article:published_time")]/@content').extract()[0]
    #     item['author'] = response.xpath('/html/head/meta[25]/@content').extract()[0]
    #
    #     item['article'] = response.xpath('//*[@id="articleBody"]/h3/text()').extract() \
    #                       + response.xpath('//*[@id="articleBody"]/p/text()').extract()
    #     item['url'] = response.xpath('/html/head/meta[@name="url"]/@content').extract()[0]
    #
    #     print('*' * 100)
    #
    #     yield item
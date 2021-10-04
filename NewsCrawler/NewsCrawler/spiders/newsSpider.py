# -*- coding: utf-8 -*-

import scrapy
from NewsCrawler.items import NewscrawlerItem
from datetime import datetime
import re
import math
import requests
from bs4 import BeautifulSoup

def get_maxpage(url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        cnt = soup.find('span',{'id' : 'resultCntArea'}).get_text()
        total_count = re.sub('[^0-9]', '', cnt.split('/')[1])
        total_pages = math.ceil(int(total_count) / 10)
        return total_pages

class NewsUrlSpider(scrapy.Spider):
    name = "newsCrawler"
    date = datetime.now().strftime('%Y%m%d')
    def start_requests(self):
        url = 'https://search.daum.net/search?w=news&DA=PGD&enc=utf8&cluster=y&cluster_page=1&q={0}&period=u&sd={1}000000&ed={1}235959&p={2}'
        # companies = ['카카오', '네이버', '삼성전자', '현대자동차', '셀트리온', 'SK 이노베이션', 'LG 에너지 솔루션', '라인', '쿠팡', '배달의 민족']
        companies =['카카오']
        

        for company in companies:
            maxpage = get_maxpage(url.format(company, self.date, 1))
        
            for page in range(1, maxpage + 1):
                yield scrapy.Request(url.format(company, self.date, page), self.parse_url)    


    def parse_url(self, response):
        for li in response.xpath('//*[@id="newsColl"]/div[1]/ul/li'):
            item = NewscrawlerItem()
            item['journal'] =  li.xpath('div[@class="wrap_cont"]/span[@class="cont_info"]/span[1]/text()').extract()[0]  # 신문사
            item['company'] = response.xpath('//*[@id="saq"]/text()').extract()[0]   # 회사
            item['title'] = li.xpath('div[@class="wrap_cont"]/a/text()').extract() # 제목
            item['date'] = self.date # 작성일
            item['newsUrl'] = li.xpath('div[@class="wrap_cont"]/a/@href').extract()[0]
            item['photoUrl'] = li.xpath('div[@class="wrap_thumb"]/a/img/@src').extract()[0]

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
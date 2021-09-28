# -*- coding: utf-8 -*-

import scrapy
import time
import csv
from NewsCrawler.items import NewscrawlerItem
import datetime
import re
import math

class NewsUrlSpider(scrapy.Spider):
    name = "newsUrlCrawler"

    def start_requests(self):
        url = 'https://search.daum.net/search?w=news&DA=STC&enc=utf8&cluster=y&cluster_page=1&q={0}&period=u&sd={1}000000&ed={1}235959&p={2}'
        companies = ['카카오', '네이버', '삼성전자', '현대자동차', '셀트리온', 'SK 이노베이션', 'LG 에너지 솔루션', '라인', '쿠팡', '배달의 민족']
        date = datetime.datetime.now().strftime('%Y%m%d')
        pages = 10

        for company in companies:
            for page in range(1, pages, 1):
                yield scrapy.Request(url.format(company, date, page),
                                     self.parse_url)

    # def parse_page(self, company, response):
    #     for text in response.xpath('//*[@id="resultCntArea"]/text()').extract():
    #         total_count = re.sub(r'[^0-9]', '', text.split('/')[1])   # 전체 기사 개수
    #         print(total_count)
    #         page_size = 10    # 1페이지 당 보여지는 기사 개수
    #         self.total_pages = math.ceil(int(total_count) / page_size)    # 전체 페이지 개수
    #
    #         for page in range(1, self.total_pages):
    #             yield scrapy.Request(self.url.format(company, self.date, page),
    #                                  self.parse_url)

    def parse_url(self, response):
        for sel in response.xpath('//*[@id="newsColl"]/div[1]/ul/li'):
            item = NewscrawlerItem()
            item['journal'] = sel.xpath('div[2]/span[1]/span/text()').extract()[0]   # 신문사
            item['company'] = response.xpath('//*[@id="saq"]/text()').extract()[0]   # 회사
            item['title'] = sel.xpath('div[@class="wrap_cont"]/a/text()').extract() # 제목
            item['date'] = datetime.datetime.now().strftime('%Y%m%d') # 작성일
            item['newsUrl'] = sel.xpath('div[@class="wrap_cont"]/a/@href').extract()[0]
            item['photoUrl'] = sel.xpath('div[@class="wrap_thumb"]/a/img/@src').extract()[0]

            # print('*' * 100)
            # print(item['title'])
            # print(item['company'])
            # print(item['journal'])
            # print(item['date'])
            # print(item['url'])
            # print(item['photo'])

            yield item

    # 전자신문 스크랩
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
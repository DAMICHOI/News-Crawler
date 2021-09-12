# -*- coding: utf-8 -*-

import scrapy
import time
import csv
from NewsCrawler.items import NewscrawlerItem

class NewsUrlSpider(scrapy.Spider):
    name = "newsUrlCrawler"

    def start_requests(self):
        press = ['024'] # 024: 경제
        pageNum = 2
        date = [20210905]

        for cp in press:
            for i in range(1, pageNum, 1):
                yield scrapy.Request("http://www.etnews.com/news/section.html?id1=02&id2={0}&page={1}".format(cp, i),
                                     self.parse_url)

    def parse_url(self, response):
        for sel in response.xpath('/html/body/div/main/div/ul[@class="list_news"]/li/dl[@class="clearfix"]'):

            yield scrapy.Request("http:"+sel.xpath('dt/a/@href').extract()[0],
                                 callback=self.parse_news)

    def parse_news(self, response):
        item = NewscrawlerItem()

        item['source'] = '전자신문'
        item['category'] = '경제'
        item['title'] = response.xpath('/html/head/meta[20]/@content').extract()[0]
        item['date'] = response.xpath('/html/head/meta[contains(@property, "article:published_time")]/@content').extract()[0]
        item['author'] = response.xpath('/html/head/meta[25]/@content').extract()[0]

        item['article'] = response.xpath('//*[@id="articleBody"]/h3/text()').extract() \
                          + response.xpath('//*[@id="articleBody"]/p/text()').extract()
        item['url'] = response.xpath('/html/head/meta[@name="url"]/@content').extract()[0]

        print('*' * 100)

        yield item
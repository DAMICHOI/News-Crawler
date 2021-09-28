# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    journal = scrapy.Field() # 신문사
    company = scrapy.Field()    # 회사명
    title = scrapy.Field()  # 제목
    date = scrapy.Field()   # 날짜
    newsUrl = scrapy.Field()    # 기사링크
    photoUrl = scrapy.Field()  # 사진링크
    pass

    # name = scrapy.Field()
    # source = scrapy.Field() # 신문사
    # category = scrapy.Field()   # 카테고리
    # title = scrapy.Field()  # 제목
    # date = scrapy.Field()   # 날짜
    # author = scrapy.Field() # 작성자
    # article = scrapy.Field()    # 기사 내용
    # url = scrapy.Field()    # 기사링크
    # pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    second_classify = scrapy.Field()  # 图书二级分类
    three_classify = scrapy.Field() # 图书三级分类
    three_href = scrapy.Field() # 图书分类链接
    book_name = scrapy.Field() # 书名
    author = scrapy.Field() # 作者
    press = scrapy.Field() # 出版社
    book_descrip = scrapy.Field() # 图书简介
    book_href = scrapy.Field() # 图书链接
    book_price = scrapy.Field() # 图书价格

    pass
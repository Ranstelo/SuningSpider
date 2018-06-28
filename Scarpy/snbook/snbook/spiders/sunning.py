# -*- coding: utf-8 -*-
import scrapy
from snbook.items import SnbookItem
import re
from copy import deepcopy

class SunningSpider(scrapy.Spider):
    name = 'sunning'

    def __init__(self):
        self.allowed_domains = ['snbook.suning.com']
        self.index_urls = "http://snbook.suning.com"
        self.start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']
        self.price_urls = "http://snbook.suning.com/web/ebook/checkPriceShowNew.do?bookId={}&completeFlag=2"
        self.page = 2

    def parse(self, response):
        li_list = response.xpath("//ul[@class='ulwrap']/li")

        for li in li_list:
            item = SnbookItem()
            item["second_classify"] = li.xpath("./div[@class='second-sort']/a/text()").extract_first()
            item["three_href"] = li.xpath("./div[@class='three-sort']/a/@href").extract()
            # item = deepcopy(item)
            for href in item["three_href"]:
                item["three_href"] = self.index_urls + href
                id = item["three_href"].split("/")[-1].split(".")[0]
                item["three_classify"] = li.xpath("./div[@class='three-sort']/a[@id={}]/text()".format(id)).extract()
                # yield item
                yield scrapy.Request(item["three_href"],callback=self.paese_books,meta={"item":deepcopy(item)})

    def paese_books(self, response):
        li_list2 = response.xpath("//ul[@class='clearfix']/li")
        item = deepcopy(response.meta["item"])
        for li in li_list2:
            item["book_name"] = li.xpath(".//div[@class='book-title']/a/text()").extract_first()
            item["book_href"] = li.xpath(".//div[@class='book-title']/a/@href").extract_first()
            item["author"] = li.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item["press"] = li.xpath(".//div[@class='book-publish']/a/text()").extract_first()
            item["book_descrip"] = li.xpath(".//div[@class='book-descrip c6']/text()").extract()
            book_id = item["book_href"].split("/")[-1].split(".")[0]
            url = self.price_urls.format(book_id)
            page_js = response.xpath("//script[@type='text/javascript']/text()").extract_first()
            pagecount = re.search(r"pagecount=(\d+);.*",page_js).group(1)
            while True:
                if self.page > int(pagecount):
                    break
                url_page = item["three_href"]+"?pageNumber={}&sort=0".format(self.page)
                self.page += 1

                yield scrapy.Request(url_page,callback=self.paese_books,meta={"item":response.meta["item"]})

            yield scrapy.Request(url,callback=self.parse_detail,meta={"item":deepcopy(item)})

    def parse_detail(self, response):
        item = response.meta["item"]
        item["book_price"] = response.xpath("//span[@class='snPrice f18 fl']/em/text()").extract_first()
        yield item
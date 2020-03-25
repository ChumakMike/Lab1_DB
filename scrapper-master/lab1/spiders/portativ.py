# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class PortativSpider(scrapy.Spider):
    name = 'portativ'
    allowed_domains = ['portativ.ua']
    start_urls = ['https://portativ.ua/naushniki-dlya-smartfona.html']

    def parse(self, response: Response):
        products = response.xpath("//div[contains(@class, 'port-i')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//img[@class='UI-CATALOG-PRODUCT-IMAGE']/@title").get(),
                'price': product.xpath(".//span[@class='price-value UAH']/@content").get(),
                'img': product.xpath(".//img[@class='UI-CATALOG-PRODUCT-IMAGE']/@src").get()
            }
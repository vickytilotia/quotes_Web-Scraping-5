# -*- coding: utf-8 -*-
import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com/js']
    start_urls = ['http://quotes.toscrape.com/js/']

    def parse(self, response):
        pass

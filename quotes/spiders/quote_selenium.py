# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy.selector import Selector

#github scrapy_seleinum is installed now.
from scrapy_selenium import SeleniumRequest
serial_number =0

class QuoteSpiderSelenium(scrapy.Spider):
    name = 'quote_selenium'
    # allowed_domains = ['quotes.toscrape.com/js']
    # start_urls = ['http://quotes.toscrape.com/js']

    def start_requests(self):
        #this is for pagination using scrapy_seleinum
        yield SeleniumRequest(
            url = "http://quotes.toscrape.com/js/",
            #missing scheme error, which required http in the url
            #so don't forget to write http in "url"
            wait_time = 3,
            screenshot = True,
            
            callback =  self.parse
        )
    
    def parse(self,response):
        global serial_number

        for q in response.xpath("//div[@class = 'quote']"):
            serial_number = serial_number + 1
            yield{
                'serial number' : serial_number,
                'author' : q.xpath(".//small[@class = 'author']/text()").get(),
                'quote' : q.xpath(".//span//text()").get(),
            }
        
        next_page = response.xpath("//li[@class = 'next']/a/@href").get()
        if next_page:
            absolute_url = f"http://quotes.toscrape.com{next_page}"
            yield SeleniumRequest(
                url = absolute_url,
                wait_time=3,
                
                callback = self.parse
            )
            
   
# To handle pagination
# Download a github repo from given link
# https://github.com/clemfromspace/scrapy-selenium
# enter this command in conda command promt
# pip install scrapy-selenium
# then follow the commands from that github repo page


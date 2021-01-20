# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy.selector import Selector


class QuoteSpiderSelenium(scrapy.Spider):
    name = 'quote_selenium'
    allowed_domains = ['quotes.toscrape.com/js']
    start_urls = ['http://quotes.toscrape.com/js']


    def __init__(self):
        #inside it we do everything releated to selenium
        chrome_options = Options()
        # chrome_options.add_argument("--headless")   # to prevent chrome from launching

        chrome_path = which("chromedriver")

        # driver = webdriver.Chrome(executable_path= chrome_path, options=chrome_options)
        driver = webdriver.Chrome(executable_path= chrome_path)
        driver.get("http://quotes.toscrape.com/js/")  

        first_quote = driver.find_element_by_class_name("text")



        self.html = driver.page_source
        # driver.close()
        print(self.html)

    
    
    
    def parse(self, response):
        resp = Selector(text = self.html)
        for q in resp.xpath("//div[@class = 'quote']"):

            yield{
                'quote' : q.xpath(".//span//text()").get(),
            }
            #we can't define the callback method into the seleinum
            #so this parse method simply not work
            #so we pass the self.html to parse method
            #but self.html is a string object so we can't directely pass it.
            #for that we use selector object
            # from scrapy.selector import Selector
            # resp = Selector(text = self.html)
            # now resp is a selector object so we can execute xpath against it
            # so we change response.xpath -> resp.xpath


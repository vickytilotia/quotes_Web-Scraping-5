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
            
        

    """def __init__(self):
        #inside it we do everything releated to selenium
        chrome_options = Options()
        # chrome_options.add_argument("--headless")   # to prevent chrome from launching

        chrome_path = which("chromedriver")

        # driver = webdriver.Chrome(executable_path= chrome_path, options=chrome_options)
        driver = webdriver.Chrome(executable_path= chrome_path)
        driver.set_window_size(1920,1080)
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
    """    
# To handle pagination
# Download a github repo from given link
# https://github.com/clemfromspace/scrapy-selenium
# enter this command in conda command promt
# pip install scrapy-selenium
# then follow the commands from that github repo page


import scrapy
import json
import re
import csv
import requests
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support import expected_conditions as EC

# from lxml import etree
# import time

import pdb

class Ecorp(scrapy.Spider):
    name = "ecorp"

    domain = "https://ecorp.azcc.gov"

    start_urls = ['https://ecorp.azcc.gov/EntitySearch/PublicSearch']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }

    cookies = {
            'BNIS_STCookie':'JDsOSUwPVldXc/Hvdmj0bNY/cYQq3q7x7qyK6gqbaSnFKLtGZYTEZQVk4PO1ccBZWyHsVZLNMoarQ0z/z8bAt8H1whZ/6f8G', 
            'x-bni-ja':'4047914012', 
            "_ga":'GA1.2.188325541.1574112530', 
            'BNES_x-bni-ja':'/Y2W+R8m8Ek3ooQPwT63u3SaWHsj2EKIhqngQLXvhFod28VUpbL9IaS6WDRzVlVO1C2Op7qo7Wo=', 
            'BNES__ga':'wYlN1YxhgGXTmmOAf4lzLgML90q1NxLOOvKAIsEbGyitKkqEosbA/B5Wtg9fCzpCJ99idyPBBewxbxclom9BaSoqb0BQGley', 
            'BNES__gid':'X96juYBOyCb5mOapud+bF0cdou2VRDkH0pGGOZujRofNmh4+gDxsoIOLXRYkKn5KC/eW3C2ifZu0R/IjfD6rrR9m2H0MHtaw',  
            'BNES__gat':'sW7NPJgIXYEY3e9bKuBRjW5/+SiDoqWDIMQMTJSbHxO5WJ9Ad7vrT4+jZfjOlSKx', 
            'ASP.NET_SessionId':'0p1qa54yxshgz4vhcrcspdbd', 
           'BNI_persistence':'VUpzTSDr1h_xUWFOwpCcVenx18NPntdyErONlshaxSQpM13CpbhUgwoI_7IExFz0B_PuqULhk4WB8vDW8Sa7UQ==', 
           'BNES_ASP.NET_SessionId':'LUf5RmDSOXSfUsc2j4qiEbc8fWiIRXlgROtFCKUS/3CZELKNgRFVjalTT8+qX7IjmPKhY9YCdgcczM+7HNmc/3WaL//8LqYdJdfJss6sqW8=',
           '_gid':'GA1.2.1945911275.1574450210', 
           'BNIS_x-bni-jas':'TdnMOKRVzRLGJ6TY+68aVzEdIXWpJsPjQQLMN8cJf0nW1f5FKq0J33ku+SeXAUAHNPEPeMjD3R4aXA9vDNn9F2juOVXYtq8GkHdrjMu47yzg2TEew24mlA==',
            '_gat':'1'
    }

    def __init__(self):
        pass
        # self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        # self.option.add_argument('blink-settings=imagesEnabled=false')
        # self.option.add_argument('--ignore-certificate-errors')
        # self.option.add_argument('--ignore-ssl-errors')
        # self.option.add_argument("--no-sandbox")
        # self.option.add_argument("--disable-impl-side-painting")
        # self.option.add_argument("--disable-setuid-sandbox")
        # self.option.add_argument("--disable-seccomp-filter-sandbox")
        # self.option.add_argument("--disable-breakpad")
        # self.option.add_argument("--disable-client-side-phishing-detection")
        # self.option.add_argument("--disable-cast")
        # self.option.add_argument("--disable-cast-streaming-hw-encoding")
        # self.option.add_argument("--disable-cloud-import")
        # self.option.add_argument("--disable-popup-blocking")
        # self.option.add_argument("--disable-session-crashed-bubble")
        # self.option.add_argument("--disable-ipv6")
        # self.driver = webdriver.Chrome(executable_path='./data/chromedriver.exe', chrome_options=self.option)

    def start_requests(self):
        yield FormRequest(
            url=self.start_urls[0],
            formdata={'SearchCriteria.quickSearch.BusinessName': 'HOMEOWNERS'},
            headers = self.headers,
            dont_filter=True,
            cookies=self.cookies,
            callback=self.parse_url
        )

    def parse_url(self, response):
        result_urls = response.xpath('//table[@id="grid_resutList"]/tbody/tr//a/@href').extract()
        for url in result_urls:
            yield Request(self.domain + url, callback=self.parse_data)
        
    def parse_data(self, response):
        pdb.set_trace()
        data_pannel1 = response.xpath('//div[@class="data_pannel1"]')

        item = ChainItem()

        # Entity Details
        item['Entity_Name'] = response.xpath('//div[@class="row"]')[1].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Entity_ID'] = response.xpath('//div[@class="row"]')[1].xpath('./div')[3].xpath('.//text()').extract_first().strip()
        item['Entity_Type'] = response.xpath('//div[@class="row"]')[2].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Entity_ID'] = response.xpath('//div[@class="row"]')[2].xpath('./div')[3].xpath('.//text()').extract()[1].strip()
        item['Formation_Date'] = response.xpath('//div[@class="row"]')[3].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Reason_for_Status'] = response.xpath('//div[@class="row"]')[3].xpath('./div')[3].xpath('.//text()').extract()[4].strip() 
        item['Approval_Date'] = response.xpath('//div[@class="row"]')[4].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Status_Date'] = response.xpath('//div[@class="row"]')[4].xpath('./div')[3].xpath('.//text()').extract_first().strip() 
        item['Original_Incorporation_Date'] = response.xpath('//div[@class="row"]')[5].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Life_Period'] = response.xpath('//div[@class="row"]')[5].xpath('./div')[3].xpath('.//text()').extract()[1].strip() 
        item['Business_Type'] = response.xpath('//div[@class="row"]')[6].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Last_Annual_Report_Filed'] = response.xpath('//div[@class="row"]')[6].xpath('./div')[3].xpath('.//text()').extract_first().strip()
        item['Domicile_State'] = response.xpath('//div[@class="row"]')[7].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Annual_Report_Due_Date'] = response.xpath('//div[@class="row"]')[7].xpath('./div')[3].xpath('.//text()').extract_first().strip() 
        item['Years_Due'] = response.xpath('//div[@class="row"]')[8].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Original_Publish_Date'] = response.xpath('//div[@class="row"]')[9].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        
        # Statutory Agent Information
        item['Name'] = response.xpath('//div[@class="row"]')[11].xpath('./div')[10].xpath('.//text()').extract_first().strip()
        item['Appointed_Status'] = response.xpath('//div[@class="row"]')[10].xpath('./div')[3].xpath('.//text()').extract_first().strip() 
        item['Attention'] = response.xpath('//div[@class="row"]')[11].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Address'] = response.xpath('//div[@class="row"]')[11].xpath('./div')[3].xpath('.//text()').extract_first().strip() 
        item['Agent_Last_Updated'] = response.xpath('//div[@class="row"]')[12].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Email'] = response.xpath('//div[@class="row"]')[12].xpath('./div')[3].xpath('.//text()').extract_first().strip() 
        item['Attention1'] = response.xpath('//div[@class="row"]')[13].xpath('./div')[1].xpath('.//text()').extract_first().strip()
        item['Mailing_Address'] = response.xpath('//div[@class="row"]')[13].xpath('./div')[3].xpath('.//text()').extract_first().strip() 
        item['Country'] = response.xpath('//div[@class="row"]')[14].xpath('./div')[1].xpath('.//text()').extract_first().strip()

        # Principal Information
        item['Principal_Information'] = item['Entity_ID'] + '_principal.csv'

        # Entity Known Place of Business
        item['Known_Place_Attention']
        yield item

    def validate(self, value):
        if value != None:
            return ' '.join(value)
        else:
            return ""




        


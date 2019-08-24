import scrapy
import json
import re
import csv
import requests
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

from lxml import etree
import time

import pdb

class Resdex(scrapy.Spider):
    name = "resdex"

    domain = "https://www.naukri.com/recruit/login"

    adv_url = "https://resdex.naukri.com/v2/search/advSearch"

    store_id = []

    login_user = ""
    login_password = ""
    search_keyword = "artificial intelligence"

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        # self.option.add_argument('blink-settings=imagesEnabled=false')
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_argument('--ignore-ssl-errors')
        self.option.add_argument("--no-sandbox")
        self.option.add_argument("--disable-impl-side-painting")
        self.option.add_argument("--disable-setuid-sandbox")
        self.option.add_argument("--disable-seccomp-filter-sandbox")
        self.option.add_argument("--disable-breakpad")
        self.option.add_argument("--disable-client-side-phishing-detection")
        self.option.add_argument("--disable-cast")
        self.option.add_argument("--disable-cast-streaming-hw-encoding")
        self.option.add_argument("--disable-cloud-import")
        self.option.add_argument("--disable-popup-blocking")
        self.option.add_argument("--disable-session-crashed-bubble")
        self.option.add_argument("--disable-ipv6")
        self.driver = webdriver.Chrome(executable_path='./data/chromedriver.exe', chrome_options=self.option)

    def start_requests(self):
        yield Request("https://stackoverflow.com/", callback=self.parse_dummy)

    def parse_dummy(self, response):
        print("New session is started ------------ ******* ----------")
        self.driver.get(self.domain)
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='toggleRCBLoginForm']/ul[@id='toggleForm']/li[2]"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "loginEmail"))).send_keys(self.login_user)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(self.login_password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()

        pdb.set_trace()
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='otpVerify']//a[@class='lt_close cPntr']"))).click()
        except:
            pass
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//ul[@id='resdexSearchesLft']/li[1]/a"))).click()
        except:
            self.driver.get(self.adv_url)
        time.sleep(2)
        try:
            try:
                WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//select/option[@title='hero.ku@disruptive-advantage.com']"))).click()
                WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='submit']"))).click()
            except:
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='quotaltCover']/button"))).click()
        except:
            pass

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul[@id='sugTagContainer']//input[@id='Sug_advKwd']"))).send_keys(self.search_keyword)
        time.sleep(1)
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='ADV_SRCH']"))).click()


        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@name="pageNo"]')))
        
        page_source = etree.HTML(self.driver.page_source)
        number_of_pages = page_source.xpath('//form[@id="topPagin"]/span[@class="txt"]/text()')[0].split('of')[1].strip()
        for j in range(int(number_of_pages) - 1):
            # pdb.set_trace()
            # if j == 1:
            #     break
            page_source = etree.HTML(self.driver.page_source)
            for data in page_source.xpath('//div[@class="tuple"]'):
                username = ' '.join(data.xpath('.//div[@class="clFx"]/a//text()'))
                mtxt = data.xpath('.//div[@class="mtxt"]')[0]
                years_experience = self.validate(mtxt.xpath('.//span[@class="exp"]/text()'))
                current_salary = self.validate(mtxt.xpath('.//span[contains(@class, "sal")]/text()'))
                current_location = self.validate(mtxt.xpath('.//span[contains(@class, "loc")]/text()'))
                current_job_role = self.validate(data.xpath('.//a[contains(@class, "designation dashTxt cDesig")]/text()'))
                current_company = self.validate(data.xpath('.//a[contains(@class, "employer dashTxt cOrg")]//text()'))
                preferred_location = self.validate(data.xpath('.//div[contains(@class, "desc locInfo")]//text()'))
                key_skills = ','.join(data.xpath('.//div[contains(@class, "desc prefSkill hKwd kSklsInfo")]/a//text()'))
                
                item = ChainItem()
                item['username'] = username
                item['years_experience'] = years_experience
                item['current_salary'] = current_salary
                item['current_location'] = current_location
                item['current_job_role'] = current_job_role
                item['current_company'] = current_company
                item['preferred_location'] = preferred_location
                item['key_skills'] = key_skills

                yield item

            WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "pgNext")]'))).click()
            
            WebDriverWait(self.driver, 500).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "pgNext")]')))

        # yield scrapy.Request(url, self.search_movie)

    def validate(self, value):
        if value != None:
            return ' '.join(value)
        else:
            return ""




        


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
import datetime
from scrapy import signals

import pdb

from scrapy.exporters import CsvItemExporter

class ChainxyPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('resdex_%s.csv' % (datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')), 'a+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['username', 'years_experience', 'current_salary', 'current_location', 'current_job_role', 'current_company', 'preferred_location', 'key_skills']
        self.exporter.start_exporting()        

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
        # row_items = [item['username'], item['years_experience'], item['current_salary'], item['current_location'], item['current_job_role'], item['current_company'], item['preferred_location'], item['key_skills']]
        # self.writer.writerow(row_items)        
        # return item
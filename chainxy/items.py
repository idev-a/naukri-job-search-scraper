# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):
    username = Field()
    years_experience = Field()
    current_salary = Field()
    current_location = Field()
    current_job_role = Field()
    current_company = Field()
    preferred_location = Field()
    key_skills = Field()
 
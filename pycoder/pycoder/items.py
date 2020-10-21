import scrapy
from scrapy.item import Field


class JobItem(scrapy.Item):
    name = Field()
    city = Field()
    min_salary = Field()
    max_salary = Field()
    company = Field()
    publish_date = Field()
    experience = Field() 
    conditions = Field()
    employment_mode = Field() #full time or part time
    schedule = Field()
    description = Field()
    responsibilities = Field()
    requirements = Field()
    skills = Field()
    url = Field()
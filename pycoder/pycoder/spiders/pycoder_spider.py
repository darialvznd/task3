import scrapy
from pycoder.items import JobItem
import re
import locale
from datetime import datetime

class HhSpider(scrapy.Spider):
    name = 'pycoder'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?st=searchVacancy&text=&specialization=1&area=95',

    ]

    def parse(self, response):
        for href in response.xpath(
                '//a[@data-qa="vacancy-serp__vacancy-title"]/@href'):
            url = response.urljoin(href.extract().split('?')[0])
            yield scrapy.Request(url, callback=self.parse_item)

        next_page = response.xpath(
            '//a[@data-qa="pager-next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        item = JobItem()

        content = response.xpath(
            '(//div[@class="main-content"]//div[contains(@class, "bloko-column_container")])[1]')
        vacancy_section = content.xpath(
            '(//div[@class="vacancy-description"]/div[@class="vacancy-section"])[1]/div[1]')
        item['name'] = content.xpath(
            './/div[contains(@class, "vacancy-title")]/h1//text()').get()

        

        xpath_t = './p/strong[contains(text(), "{}")]/ancestor::p/following::ul[1]/li/text()'

        responsibilities = vacancy_section.xpath(xpath_t.format(
            'Обязанности')).getall()

        s = ' '.join(responsibilities).replace(',', ';')
        item['responsibilities'] = s

        # item['responsibilities'] = vacancy_section.xpath(xpath_t.format(
        #     'Обязанности')).extract_first().replace(',', '')
        requirements = vacancy_section.xpath(
            xpath_t.format('Требования')).getall()
        s = ' '.join(requirements).replace(',', ';')
        item['requirements'] = s
        # item['requirements'] = vacancy_section.xpath(xpath_t.format(
        #     'Требования')).extract_first()
        conditions = vacancy_section.xpath(xpath_t.format(
            'Условия')).getall()
        s = ' '.join(conditions).replace(',', ';')
        item['conditions'] = s
        # item['conditions'] = vacancy_section.xpath(xpath_t.format(
        #     'Условия')).extract_first()
        salary = content.xpath(
                    './/p[@class="vacancy-salary"]//*/text()').getall()

        for i in range(len(salary)):
            # salary[i+1]
            if (salary[i] == 'от '):
                item['min_salary'] =  re.sub(r'\s', '', salary[i+1])
            if (salary[i] == ' до ' or salary[i] == 'до '): 
                item['max_salary'] = re.sub(r'\s', '', salary[i+1])

        item['publish_date'] = content.xpath(
            './/p[@class="vacancy-creation-time"]//text()').getall()[1]
       
      
        
        
        company = content.xpath(
            './/a[@data-qa="vacancy-company-name"]//*/text()').getall()
        s = ' '.join(company).replace(',', '')
        item['company'] = s

        item['city'] = content.xpath(
            './/p[@data-qa="vacancy-view-location"]//text()').extract_first().split(',', 1)[0]
        item['experience'] = content.xpath(
            './/*[@data-qa="vacancy-experience"]//text()').getall()

        employment_mode = content.xpath(
            './/*[@data-qa="vacancy-view-employment-mode"]//text()'
        ).getall()
        item['employment_mode'] = employment_mode[0]
        item['schedule'] = employment_mode[-1]
        skills = content.xpath(
            './/*[contains(@data-qa, "skills-element")]/span/text()'
        ).getall()

        s = ';'.join(skills)
        item['skills'] = s
        # item['skills'] =  content.xpath(
        #     './/*[contains(@data-qa, "skills-element")]/span/text()'
        #     ).extract()

        # for i in range (len(skills))):
        #     item['skills'].append(skills[i])

        item['description'] = vacancy_section.get() or ""
        item['url'] = response.request.url

        yield item


#cd pycoder
#scrapy crawl pycoder -o data.csv
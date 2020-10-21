# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import lxml.html.clean as clean
import re



class PycoderPipeline:
    def process_item(self, item, spider): 
        print("######################################################################м##")
        return item



class JobPipeline(object):

    def __init__(self):
        self.cleaner = clean.Cleaner(style=True, links=True,
            add_nofollow=True, page_structure=False, safe_attrs=[],
            remove_tags=['svg', 'img'])

    def clean_html(self, html):
        if (html == ''):
            return html
        html = self.cleaner.clean_html(html)
        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r',', ' ', html)
        html = html.replace('\n\r', ' ')
        return re.sub(r'</?\w+>', '', html)

    def process_item(self, item, spider):
        item['description'] = self.clean_html(item['description'])
       
        # for i in range (len(item['company'])):
        #     item['company'][i] = item['company'][i].replace(',', '')
        # item['salary'] = 
        return item

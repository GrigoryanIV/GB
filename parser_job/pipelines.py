# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from http import client
#from typing import Collection

from pymongo import MongoClient
from scrapy.loader import ItemLoader

class ParserJobPipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.parser_job
        
    
    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        if collection.find_one({'_id': item['_id']}) == None:
            collection.insert_one(item)
        
        return item

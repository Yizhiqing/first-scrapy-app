# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import sqlite3
import os


class TutorialPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('output.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

con = None
class DatabasePipeline(object):
    def __init__(self):
        self.setupDBCon()
        self.createTables()
        
    def setupDBCon(self):
        self.con = sqlite3.connect(os.getcwd() + '/test.db')
        self.cur = self.con.cursor()
    
    def createTables(self):
        self.dropAmazonTable()
        self.createAmazonTable()
    
    def dropAmazonTable(self):
        #drop amazon table if it exists
        self.cur.execute("DROP TABLE IF EXISTS Amazon")
    
    def closeDB(self):
        self.con.close()
        
    def __del__(self):
        self.closeDB()
        
    def createAmazonTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Amazon(id INTEGER PRIMARY KEY NOT NULL, \
            house_name TEXT, \
            address TEXT, \
            transport TEXT \
            )")
    
    
    def process_item(self, item, spider):
        self.storeInDb(item)
        return item

    def storeInDb(self,item):
        self.cur.execute("INSERT INTO Amazon(\
            house_name, \
            address, \
            transport \
            ) \
        VALUES( ?, ?, ?)", \
        ( \
            item.get('house_name',''),
            item.get('address',''),
            item.get('transport','')
        ))
        print('------------------------')
        print('Data Stored in Database')
        print('------------------------')
        self.con.commit()                    

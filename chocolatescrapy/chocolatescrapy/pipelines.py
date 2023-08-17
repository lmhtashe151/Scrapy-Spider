# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector
import psycopg2


class ChocolatescrapyPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gdpToUSDRate = 1.3
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            floatPrice = float(adapter['price'])
            adapter['price'] = floatPrice * self.gdpToUSDRate
            return item 
        else:
            raise DropItem(f"Missing price in {item}")


class DuplicatesPipeline:
    def __init__(self):
        self.name_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.name_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.name_seen.add(adapter['name'])
            return item
        
class SavingToMysqlPineline(object):
    def __init__(self):
        self.create_connection()
    
    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'dogbig151',
            database = 'chocolate_scraping',
            port = '3306'
        )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
    def store_db(self, item):
        self.curr.execute(""" insert into chocolate_products (name, price, url) values (%s,%s,%s) """,(
            item["name"],
            item["price"],
            item["url"]
        ))
        self.connection.commit()

class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()
    
    def create_connection(self):
        self.connection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '12345678',
            database = 'chocolate_scraping',
        )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
    def store_db(self, item):
        try:
            self.curr.execute(""" insert into chocolate_products (name, price, url) values (%s,%s,%s) """,(
                item["name"],
                item["price"],
                item["url"]
            ))
        except BaseException as e:
            print(e)

        self.connection.commit()
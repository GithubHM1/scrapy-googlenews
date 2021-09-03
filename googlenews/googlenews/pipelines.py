# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class GooglenewsPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            user='',
            password='',
            host='',
            port=,
            database=''
        )

        self.curr = self.conn.cursor()
    
    # 'start','end','query', 'region', 'title', 'excerpt', 'date', 'source', 'link' 
    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS semiconductor8a(
            id INT AUTO_INCREMENT PRIMARY KEY,
            query TEXT,
            region VARCHAR(255),
            title TEXT,
            excerpt TEXT,
            date DATE,
            source VARCHAR(255),
            link VARCHAR(255),
            tokens TEXT,
            stemmed TEXT,
            lemmatized TEXT,
            sentiment FLOAT,
            subjective FLOAT
        )""")

    def process_item(self, item, spider):
        self.store_db(item)

    def store_db(self, item):
        myquery = """INSERT into semiconductor8a
        (
            query,
            region,
            title,
            excerpt,
            date,
            source,
            link,
            tokens,
            stemmed,
            lemmatized,
            sentiment,
            subjective
        )
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        value = (
            item['query'][0],
            item['region'][0],
            item['title'],
            item['excerpt'][0],
            item['date'],
            item['source'],
            item['link'],
            item['tokens'][0],
            item['stemmed'][0],
            item['lemmatized'][0],
            item['sentiment'],
            item['subjective']
        )

        self.curr.execute(myquery, value)
        self.conn.commit()
    
    def close_spider(self, spider):
        self.conn.close

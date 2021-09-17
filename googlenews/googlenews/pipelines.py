# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector

class DuplicatesPipeline:

    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.titles_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.titles_seen.add(adapter['title'])
            return item

class GooglenewsPipeline(object):
    duplicatelist =[]

    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            user='',
            password='',
            host='',
            port=,
            database='',
        )

        self.curr = self.conn.cursor()
    
    # 'start','end','query', 'region', 'title', 'excerpt', 'date', 'source', 'link' 
    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS semiconductor8b(
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
        self.check_duplicate(item)
        self.store_db(item)

    def check_duplicate(self, item):
        newTitle = item['title']
        newSource = item['source']
        findquery = """ SELECT title FROM semiconductor8b WHERE title = %s AND source = %s """

        self.curr.execute(findquery,(newTitle,newSource))

        for x in self.curr:
            self.duplicatelist.append(x)


    def store_db(self, item):

        insertquery = """INSERT into semiconductor8b
        (
            query,
            region,
            title ,
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

        if len(self.duplicatelist) > 0:
            print(str(len(self.duplicatelist)) + " duplicate(s) found")
        else:
            self.curr.execute(insertquery, value)
            self.conn.commit()
            
    
    def close_spider(self, spider):
        self.conn.close

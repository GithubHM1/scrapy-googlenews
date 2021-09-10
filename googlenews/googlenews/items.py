# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import datetime

# activate this part ONLY when scrap from rss
# def split_date(value):
#     newdate = value.split()
#     return newdate[1] + ' ' + newdate[2] + ' ' + newdate[3]

month={
    "Jan":"1",
    "Feb":"2",
    "Mar":"3",
    "Apr":"4",
    "May":"5",
    "Jun":"6",
    "Jul":"7",
    "Aug":"8",
    "Sep":"9",
    "Oct":"10",
    "Nov":"11",
    "Dec":"12"
}

modifier = 0

def preconvert_date(value):
    global new_date
    today = datetime.date.today()
    day_differences = modifier*int(value)
    date_reducer = datetime.timedelta(days = day_differences)
    new_date = (today - date_reducer).strftime('%Y-%m-%d')


def convert_pubdate(value):
    global new_date
    global modifier
    old_date = value.split()
    
    if 'hour' in value or 'hours' in value:
        preconvert_date(old_date[0])
    elif 'day' in value or 'days' in value:
        modifier += 7
        preconvert_date(old_date[0])
    elif 'week' in value or 'weeks' in value:
        modifier += 7
        preconvert_date(old_date[0])
    elif 'month' in value or 'months' in value:
        modifier += 30
        preconvert_date(old_date[0])
    else:
        new_date = old_date[2] + "-" + month(old_date[1]) + "-" + old_date[0]

    return new_date

def strip_value(value):
    newText1 = value.strip('...')
    return newText1


class GooglenewsItem(scrapy.Item):
    # define the fields for your item here:
    query = scrapy.Field()
    region = scrapy.Field()
    title = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    date = scrapy.Field(input_processor = MapCompose(remove_tags,convert_pubdate), output_processor = TakeFirst())
    source = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    link = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    excerpt = scrapy.Field(input_processor = MapCompose(remove_tags,strip_value))
    tokens = scrapy.Field()
    stemmed = scrapy.Field()
    lemmatized = scrapy.Field()
    sentiment = scrapy.Field(output_processor = TakeFirst())
    subjective = scrapy.Field(output_processor = TakeFirst())
    # start = scrapy.Field(input_processor = MapCompose(convert_month), output_processor = TakeFirst())
    # end = scrapy.Field(input_processor = MapCompose(convert_month), output_processor = TakeFirst())
    

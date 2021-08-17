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

def strip_item(value):
    excerpt = value.strip(",")
    return excerpt

def convert_month(value):
    old_date = value.split("/")
    new_date = old_date[2] + "-" + old_date[0] + "-" + old_date[1]

    return new_date
    
def convert_pubdate(value):
    modifier = 0
    old_date = value.split()
    day_differences = modifier*int(old_date[0])
    today = datetime.date.today()
    date_reducer = datetime.timedelta(days = day_differences)
    if 'hour' in value or 'hours' in value:
        new_date = (today - date_reducer).isoformat
    elif 'day' in value or 'days' in value:
        modifier=1
        new_date = (today - date_reducer).isoformat
    elif 'week' in value or 'weeks' in value:
        modifier=7
        new_date = (today - date_reducer).isoformat
    elif 'month' in value or 'months' in value:
        modifier=30
        new_date = (today - date_reducer).isoformat
    else:
        new_date = old_date[2] + "-" + month[old_date[1]] + "-" + old_date[0]
    
    return new_date


class GooglenewsItem(scrapy.Item):
    # define the fields for your item here like:
    query = scrapy.Field()
    region = scrapy.Field()
    title = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    date = scrapy.Field(input_processor = MapCompose(remove_tags, convert_pubdate), output_processor = TakeFirst())
    source = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    link = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    excerpt = scrapy.Field(input_processor = MapCompose(strip_item, remove_tags), output_processor = TakeFirst())
    start = scrapy.Field(input_processor = MapCompose(convert_month), output_processor = TakeFirst())
    end = scrapy.Field(input_processor = MapCompose(convert_month), output_processor = TakeFirst())
    

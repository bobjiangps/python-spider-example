# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDoubanItem(scrapy.Item):
    title = scrapy.Field()
    publish = scrapy.Field()
    score = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FreebieItem(scrapy.Item):
    title = scrapy.Field(serializer=str)
    product_url = scrapy.Field(serializer=str)
    file_format = scrapy.Field(serializer=str)
    file_size = scrapy.Field(serializer=int)
    file_dimensions = scrapy.Field(serializer=dict)
    images = scrapy.Field(serializer=list)
    preview_images = scrapy.Field(serializer=list)
    description = scrapy.Field(serializer=str)

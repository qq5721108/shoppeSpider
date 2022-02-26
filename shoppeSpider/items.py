# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoppespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemid = scrapy.Field()
    shopid = scrapy.Field()
    price = scrapy.Field()
    price_max = scrapy.Field()
    liked_count = scrapy.Field()
    price_min = scrapy.Field()
    discount = scrapy.Field()
    sold = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    attributes = scrapy.Field()
    tier_variations = scrapy.Field()
    categories = scrapy.Field()
    categories_name = scrapy.Field()
    catid = scrapy.Field()
    ctime = scrapy.Field()
    rating_star = scrapy.Field()
    rating_count = scrapy.Field()
    image = scrapy.Field()

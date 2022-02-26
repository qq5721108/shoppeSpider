# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from shoppeSpider.MySql import MySql


class ShoppespiderPipeline:
    mysql = MySql()

    def process_item(self, item, spider):
        try:
            self.mysql.insert_db(item)
            # self.myRedis.insert_redis(item)
        except Exception as e:
            print("异常--", e)
        return item

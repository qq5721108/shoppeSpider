# -*- coding: utf-8 -*-
import pymysql
from shoppeSpider import settings


class MySql(object):

    db = pymysql.connect(host="101.35.132.138", user=settings.DB_USERNAME, password=settings.DB_PASSWORD, database=settings.DB_NAME, charset='utf8')
    cursor = db.cursor()

    def __init__(self):
        pass

    def insert_db(self, item):
        sql = """INSERT INTO shoppe_sg(itemid, shopid, price, price_max, liked_count, price_min, discount, sold, name,
         description, attributes, tier_variations, categories_name, rating_star, 
         rating_count, catid, categories, ctime, image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (item['itemid'],
                  item['shopid'],
                  item['price'], item['price_max'],
                  item['liked_count'], item['price_min'], item['discount'], item['sold'], item['name'], item['description'],
                  item['attributes'], item['tier_variations'], item['categories_name'],
                  item['rating_star'],  item['rating_count'], item['catid'], item['categories'], item['ctime'], item['image'])
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise

    def select_item_db(self):
        sql = "SELECT itemid FROM product"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def select_num_db(self):
        sql = "SELECT COUNT(id) FROM product"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def __del__(self):
        self.db.close()
        pass
import redis

from shoppeSpider.MySql import MySql


class MyRedis:
    redis_db = redis.Redis(host="101.35.132.138", port=6379, db=0)
    redis_data_dict = 'itemid'
    mysql = MySql()

    def __init__(self):
        dbsize = self.mysql.select_num_db()
        rdsize = self.redis_db.scard(self.redis_data_dict)
        if dbsize != rdsize:
            self.redis_db.flushdb()
            if self.redis_db.hlen(self.redis_data_dict) == 0:
                data = self.mysql.select_item_db();
                for itemId in data:
                    self.redis_db.sadd(self.redis_data_dict, itemId[0])

    def is_exit(self, itemId):
        if self.redis_db.sismember(self.redis_data_dict, itemId):
            print(itemId, ':--exit')
            return False
        else:
            return True

    def insert_redis(self, itemId):
        self.redis_db.sadd(self.redis_data_dict, itemId)

    def __del__(self):
        pass
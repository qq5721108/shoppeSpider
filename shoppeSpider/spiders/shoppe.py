import json
import scrapy

from shoppeSpider.items import ShoppespiderItem


class ShoppeSpider(scrapy.Spider):
    name = 'shoppe'
    start_urls = ['https://shopee.sg/Men\'s-wear-cat.11012963']

    def __init__(self):
        self.allowed_domains = ['shopee.sg']
        # 类别api
        self.category_tree_list_url = "https://shopee.sg/api/v4/pages/get_category_tree"
        # 根据类别拉取数据api
        self.search_items = "https://shopee.sg/api/v4/search/search_items?by=relevancy&limit=60"
        self.get_url = "https://shopee.sg/api/v4/item/get?"
        self.start_urls = [self.category_tree_list_url]

    def parse(self, response):
        parent_category_list = json.loads(response.body)['data']['category_list']
        for data in parent_category_list:
            return self.parse_subcategory(data['children'])

    def parse_subcategory(self, child_category_list):
        for data in child_category_list:
            url = self.search_items + "&newest=1&order=desc&match_id={}".format(data['catid'])
            yield scrapy.Request(url, callback=self.parse_search, meta={'catid': data['catid'], 'newest':0})

    def parse_search(self, response):
        cat_id = response.meta['catid']
        newest = response.meta['newest']
        data_list = json.loads(response.body)['items']
        if len(data_list) == 0:
            return
        for data in data_list:
            item = data['item_basic']
            url = self.get_url + "itemid={}&shopid={}".format(data['itemid'], data['shopid'])
            yield scrapy.Request(url, callback=self.parse_items, meta={'itemid': data['itemid']})
        next_page_url = self.search_items + "&newest={}&match_id={}".format(newest+60, cat_id)
        yield scrapy.Request(url, callback=self.parse_search, meta={'catid': cat_id, 'newest': newest + 60})

    def parse_items(self, response):
        item_data = json.loads(response.body, encoding='utf-8')['data']
        if len(item_data) == 0:
            return
        item = ShoppespiderItem()
        item['itemid'] = item_data['itemid']
        item['shopid'] = item_data['shopid']
        item['price'] = round(item_data['price']/1000000, 2)
        if item_data['price_max'] == -1:
            item['price_max'] = 0
        else:
            item['price_max'] = round(item_data['price_max']/1000000, 2)
        if item_data['price_min'] == -1:
            item['price_min'] = 0
        else:
            item['price_min'] = round(item_data['price_min']/1000000, 2)
        item['liked_count'] = item_data['liked_count']
        item['rating_star'] = item_data['item_rating']['rating_star']
        item['rating_count'] = ','.join(map(str, item_data['item_rating']['rating_count']))
        item['catid'] = item_data['catid']
        categories = []
        categories_name = []
        for catId in item_data['categories']:
            categories.append(catId['catid'])
            categories_name.append(catId['display_name'])
        item['categories'] = ','.join(map(str, categories))
        item['categories_name'] = ','.join(map(str, categories_name))
        item['ctime'] = item_data['ctime']
        item['sold'] = item_data['sold']
        item['image'] = item_data['image']
        yield item

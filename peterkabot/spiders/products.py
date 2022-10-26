import json
import scrapy
from scrapy.http.request.json_request import JsonRequest


class ProductsSpider(scrapy.Spider):
    name = 'products'

    def start_requests(self):
        self.url = 'https://products.5-delivery.ru/api/products/list'
        self.query = {
            "page": 1,
            "stock": 3737,  # 899
            "region": 1,
            "lpage": 200
        }
        yield JsonRequest(url=self.url, method="POST", data=self.query, callback=self.parse)

    def parse(self, response):

        res = json.loads(response.body)
        products = res["ANS"]["products"]

        for product in products:
            yield {
                "discount": round(product["sale_props"]["sale_percent"]),
                "name": product["name"],
                "weight_volume_price": f"1 кг / {product['price']} руб" if product["by_weight"]["use"] else f"1 шт / {product['price']} руб",
                "price": round(product["price"] * product["boxsize"], 2),
                "old_price": round(product["sale"] * product["boxsize"], 2) if product["sale"] > 0 else "Отсутствует",
                "image_link": f"https://photos.5-delivery.ru/big{product['img']}",
            }

        next_page = res["ANS"]["nav"]['next']

        if next_page:
            self.query["page"] = next_page
            yield JsonRequest(url=self.url, method="POST", data=self.query, callback=self.parse)

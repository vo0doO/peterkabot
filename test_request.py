import requests
import json

data = {
    "page": "1",
    "stock": "3737",
    "region": "1",
    "lpage": "200"
}

url = 'https://products.5-delivery.ru/api/products/list'

res = requests.post(url, data=data)

print(res.json())

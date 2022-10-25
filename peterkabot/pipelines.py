# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import json
from scrapy.exceptions import DropItem


class PeterkabotPipeline:
    def process_item(self, item, spider):
        return item


class CsvWriterPipeline:

    def open_spider(self, spider):
        self.fieldnames = [
            'discount', 'name', 'weight_volume_price',
            'price', 'old_price', 'image_link'
        ]
        self.file = open(
            f"{spider.name}.csv", mode="w",
            newline="", encoding='utf-8'
        )
        self.writer = csv.DictWriter(
            self.file, fieldnames=self.fieldnames, dialect='excel-tab'
        )
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item


class DublicatesPipeLine:

    def __init__(self):
        self.name_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.name_seen:
            raise DropItem(f"Обнаружен  дубликат ==> {item}")
        else:
            self.name_seen.add(item["name"])
            return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open(f"{spider.name}.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item, ensure_ascii=False,) + "\n"
        self.file.write(line)
        return item

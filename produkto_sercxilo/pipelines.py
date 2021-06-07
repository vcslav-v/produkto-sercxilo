# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import json

import requests
from requests.auth import HTTPBasicAuth

from produkto_sercxilo import models

from produkto_sercxilo.db import SessionLocal
from produkto_sercxilo.schemas import FabItem
from os import environ

AUTH_LOG = environ.get('AUTH_LOG')
AUTH_PASS = environ.get('AUTH_PASS')
FAB_URL = environ.get('FAB_URL')


class ProduktoSercxiloPipeline:

    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        data = '[{data}]'.format(data=', '.join(self.items))
        requests.post(
            FAB_URL,
            data=data,
            auth=HTTPBasicAuth(AUTH_LOG, AUTH_PASS),
        )

    def process_item(self, item, spider):
        session = SessionLocal()
        fab_item = FabItem.parse_raw(json.dumps(dict(item)))
        if not self.is_exist(fab_item, session):
            self.push_to_db(fab_item, session)
            self.items.append(fab_item.json())
        session.close()
        return item

    def is_exist(self, item: FabItem, session):
        exist_item = session.query(models.FabItem).filter_by(
            product_url=item.product_url
        ).first()
        if exist_item:
            return True
        return False

    def push_to_db(self, item: FabItem, session):
        new_item = models.FabItem(
            title=item.title,
            product_url=item.product_url,
            file_format=item.file_format,
            file_size=item.file_size,
            description=item.description,
            file_dimensions_width=item.file_dimensions.width if item.file_dimensions else None,
            file_dimensions_height=item.file_dimensions.height if item.file_dimensions else None,
        )

        if item.images:
            for img in item.images:
                new_img = models.Image(
                    url=img.source,
                    alt=img.alt,
                )
                session.add(new_img)
                new_item.images.append(new_img)

        if item.preview_images:
            for img in item.preview_images:
                new_img = models.Image(
                    url=img.source,
                    alt=img.alt,
                    preview=True,
                )
                session.add(new_img)
                new_item.images.append(new_img)

        session.add(new_item)
        session.commit()

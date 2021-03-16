# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from produkto_sercxilo.db import SessionLocal
from produkto_sercxilo import models
import requests


class ProduktoSercxiloPipeline:
    def process_item(self, item, spider):
        if not self.is_exist_in_db_make_if_not(item):
            self.sent_to_fab(item)
        return item

    def is_exist_in_db_make_if_not(self, item):
        session = SessionLocal()
        exist_item = session.query(models.FabItem).filter_by(
            product_url=item['product_url']
        ).first()
        print(exist_item)
        if exist_item:
            return True

        new_item = models.FabItem(
            title=item.get('title'),
            product_url=item.get('product_url'),
            file_format=item.get('file_format'),
            file_size=item.get('file_size'),
            description=item.get('description'),
        )

        if item.get('file_dimensions'):
            new_item_dimensions = models.ItemDimension(
                width=item.get('file_dimensions').get('width'),
                height=item.get('file_dimensions').get('height'),
            )
            session.add(new_item_dimensions)
            new_item.file_dimensions = new_item_dimensions

        if item.get('images'):
            for img in item.get('images'):
                new_img = models.Image(
                    url=img['source'],
                    alt=img['alt'],
                )
                session.add(new_img)
                new_item.images.append(new_img)

        if item.get('preview_images'):
            for img in item.get('preview_images'):
                new_img = models.Image(
                    url=img['source'],
                    alt=img['alt'],
                    preview=True,
                )
                session.add(new_img)
                new_item.images.append(new_img)

        session.add(new_item)
        session.commit()
        session.close()
        return False

    def sent_to_fab(self, item):
        # requests.post('https://httpbin.org/post', data={'key':'value'})
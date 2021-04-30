# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from produkto_sercxilo.db import SessionLocal
from produkto_sercxilo import models
import requests


class ProduktoSercxiloPipeline:
    def process_item(self, item, spider):
        session = SessionLocal()
        if not self.is_exist(item, session):
            self.push_to_db(item, session)
            self.sent_to_fab(item)
        session.close()
        return item

    def is_exist(self, item, session):
        exist_item = session.query(models.FabItem).filter_by(
            product_url=item['product_url']
        ).first()
        if exist_item:
            return True
        return False

    def push_to_db(self, item, session):
        new_item = models.FabItem(
            title=item.get('title'),
            product_url=item.get('product_url'),
            file_format=item.get('file_format'),
            file_size=item.get('file_size'),
            description=item.get('description'),
            file_dimensions_width=item.get('file_dimensions').get('width') if item.get('file_dimensions') else None,
            file_dimensions_height=item.get('file_dimensions').get('height') if item.get('file_dimensions') else None,
        )

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

    def sent_to_fab(self, item):
        pass
        # requests.post('https://httpbin.org/post', data={'key':'value'})

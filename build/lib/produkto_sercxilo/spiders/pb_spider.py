import html2text
import scrapy
from produkto_sercxilo.items import FreebieItem
import re


class PbSpiderSpider(scrapy.Spider):
    name = 'pb_spider'
    allowed_domains = ['pixelbuddha.net']
    start_urls = ['https://pixelbuddha.net/mockups/']

    def start_requests(self):
        page_url = 'https://pixelbuddha.net/mockups/'
        yield scrapy.Request(page_url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath(
            '//div[@class="post-item"]//a[@class="post-image-wrapper"]/@href'
        ).extract():

            preview_xpath = (
                '//a[@href="{href}" and @class="post-image-wrapper"]//img'.format(
                    href=href
                )
            )

            item_url = response.urljoin(href)
            preview_url = response.xpath(
                    '{preview_xpath}/@src'.format(
                        preview_xpath=preview_xpath
                    )
                ).get()
            preview_url = response.urljoin(preview_url)
            preview_images = [{
                'source': preview_url,
                'alt': response.xpath(
                    '{preview_xpath}/@alt'.format(
                        preview_xpath=preview_xpath
                    )
                ).get(),
            }]
            yield scrapy.Request(
                item_url,
                cb_kwargs={'preview_images': preview_images},
                callback=self.parse,
            )

    def parse(self, response, **kwards):
        item = FreebieItem()
        item['title'] = response.xpath(
            '//h1[@class="section-header-headline"]/text()'
        ).get().strip()
        item['product_url'] = response.url

        main_img_url = response.xpath(
                '//img[@class="freebie-image-main-wrapper"]/@src'
            ).get()
        main_img_url = response.urljoin(main_img_url)
        item['images'] = [{
            'source': main_img_url,
            'alt': response.xpath(
                '//div[@class="hover-wrap-inner"]/img/@alt'
            ).get(),
        }]

        for sub_img_url in response.xpath(
            '//div[@class="freebie-images-sub"]//img/@src'
        ).extract():
            sub_img_alt = response.xpath(
                '//img[@src="{src}"]/@alt'.format(src=sub_img_url)
            ).get()
            sub_img_url = response.urljoin(sub_img_url)
            item['images'].append(
                {
                    'source': sub_img_url,
                    'alt': sub_img_alt
                }
            )

        item['preview_images'] = kwards['preview_images']
        item['description'] = self.flat_html(response.xpath(
            '//div[@class="text-block"]/div'
        ).extract())

        item['file_format'] = response.xpath(
            '//span[contains(.,"Format:")]/../span[@class="list-description-value"]/text()'
        ).get().strip()
        item['file_size'] = self.get_file_size(
            response.xpath(
                '//span[contains(.,"Size:")]/../span[@class="list-description-value"]/text()'
            ).get().strip()
        )
        yield item

    def flat_html(self, html):
        flatter = html2text.HTML2Text()
        flatter.ignore_links = True
        html = ' '.join(html)
        return flatter.handle(html).replace('\n', ' ').strip()

    def get_file_size(self, raw_text):
        raw_text = raw_text.lower()
        megabytes = re.search(r'\d+', raw_text).group(0)
        if megabytes is not None:
            return int(megabytes)

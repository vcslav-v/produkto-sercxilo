import html2text
import re
import scrapy
from produkto_sercxilo.items import FreebieItem


class AnthonyboydSpiderSpider(scrapy.Spider):
    name = 'anthonyboyd_spider'
    allowed_domains = ['anthonyboyd.graphics']
    start_urls = ['https://www.anthonyboyd.graphics/mockups/']
    pages_count = 2

    def start_requests(self):
        yield scrapy.Request(
            'https://www.anthonyboyd.graphics/mockups/',
            callback=self.parse_pages,
        )
        for page in range(2, 1 + self.pages_count):
            page_url = (
                'https://www.anthonyboyd.graphics/mockups/{page}/'.format(
                    page=page
                )
            )
            yield scrapy.Request(page_url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath(
            '//div[@class="simple-post-wrapper"]//a/@href'
        ).extract():
            preview_xpath = (
                '//div[@class="simple-post-wrapper"]/a[@href="{href}"]'.format(
                    href=href
                ) + '//picture/img/@{attr}'
            )
            item_url = response.urljoin(href)
            preview_url = response.xpath(preview_xpath.format(
                attr='src'
            )).get()
            preview_url = response.urljoin(preview_url)
            preview_alt = response.xpath(preview_xpath.format(
                attr='alt'
            )).get()
            preview_images = [{
                'source': preview_url,
                'alt': preview_alt,
            }]
            yield scrapy.Request(
                item_url,
                cb_kwargs={'preview_images': preview_images},
                callback=self.parse,
            )

    def parse(self, response, **kwards):
        item = FreebieItem()
        item['title'] = response.xpath(
            '//h2[@class="resource-post-title"]/text()'
        ).get().strip()
        item['product_url'] = response.url

        image_xpath = '//div[@class="resource-gallery-wrapper"]//img/@{attr}'
        image_url = response.xpath(
                image_xpath.format(attr='src')
            ).get()
        image_url = response.urljoin(image_url)
        image_alt = response.xpath(
            image_xpath.format(attr='alt')
        ).get()
        item['images'] = [{
            'source': image_url,
            'alt': image_alt,
        }]
        item['preview_images'] = kwards['preview_images']
        item['description'] = self.flat_html(response.xpath(
            '//div[@class="resource-post-description"]/p'
        ).get())
        item['file_format'] = response.xpath('//p[contains(.,"File Format:")]/text()').get().strip()
        item['file_size'] = self.get_file_size(
            response.xpath('//p[contains(.,"File Size:")]/text()').get()
        )
        item['file_dimensions'] = self.get_file_dimensions(
            response.xpath('//p[contains(.,"Dimensions:")]/text()').get()
        )

        yield item

    def flat_html(self, html):
        flatter = html2text.HTML2Text()
        flatter.ignore_links = True
        return flatter.handle(html).replace('\n', ' ').strip()

    def get_file_size(self, raw_text):
        raw_text = raw_text.lower()
        megabytes = re.search(r'\d+', raw_text).group(0)
        if megabytes is not None:
            return int(megabytes)

    def get_file_dimensions(self, raw_text):
        width_height = re.findall(r'\d+', raw_text)
        if not width_height or len(width_height) != 2:
            return
        width, height = width_height
        return {
            'width': int(width),
            'height': int(height),
        }

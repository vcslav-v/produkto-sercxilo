import html2text
import scrapy
from produkto_sercxilo.items import FreebieItem


class MrmockupSpiderSpider(scrapy.Spider):
    name = 'mrmockup_spider'
    allowed_domains = ['mrmockup.com']
    start_urls = ['http://mrmockup.com/freebies/']
    pages_count = 2

    def start_requests(self):
        for page in range(1 + self.pages_count):
            page_url = (
                'https://mrmockup.com/freebies/page/{page}/'.format(page=page)
            )
            yield scrapy.Request(page_url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath(
            '//div[@class="content-inner"]/a/@href'
        ).extract():
            item_url = response.urljoin(href)
            preview_xpath = (
                '//a[@href="{href}" and @class="img-link"]//img'.format(
                    href=item_url
                )
            )
            preview_images = [{
                'source': response.xpath(
                    '{preview_xpath}/@data-nectar-img-src'.format(
                        preview_xpath=preview_xpath
                    )
                ).get(),
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
            '//h1[@class="entry-title"]/text()'
        ).get().strip()
        item['product_url'] = response.url
        item['images'] = [{
            'source': response.xpath(
                '//div[@class="hover-wrap-inner"]/img/@src'
            ).get(),
            'alt': response.xpath(
                '//div[@class="hover-wrap-inner"]/img/@alt'
            ).get(),
        }]
        item['preview_images'] = kwards['preview_images']
        item['description'] = self.flat_html(response.xpath(
            '//div[@class="wpb_wrapper"]/p'
        ).get())
        yield item

    def flat_html(self, html):
        flatter = html2text.HTML2Text()
        flatter.ignore_links = True
        return flatter.handle(html).replace('\n', ' ').strip()

from scrapy.http.response import Response
import scrapy


class ISportSpider(scrapy.Spider):
    name = 'isport'
    allowed_domains = ['isport.ua']
    start_urls = ['https://isport.ua/']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@data-src[starts-with(., 'http')]")
        all_text = response.xpath("//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > "
                                  "30]/text()")
        yield {
            'url': response.url,
            'payload': [{'type': 'text', 'data': text.get().strip()} for text in all_text] +
                       [{'type': 'image', 'data': image.get()} for image in all_images]
        }
        if response.url == self.start_urls[0]:
            all_links = response.xpath(
                "//a/@href[starts-with(., '/')]")
            selected_links = ['https://isport.ua'
                              '' + link.get() for link in all_links][:20]
            for link in selected_links:
                yield scrapy.Request(link, self.parse)
import scrapy
from tutorial.items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://suumo.jp/chintai/tokyo/ek_25620/?po1=25&et=15&vos=op4031yhsstw012000000zzz_01x0013524-xb_kwd-305533245293:cr-283516076133:sl-:adg-49440702132:cam-351122192&ipao9700=YSS&ipao9701=b&ipao9702=%E8%B3%83%E8%B2%B8%20%E6%9D%B1%E4%BA%AC%E9%A7%85&ipao9703=c&ipao9704=283516076133&ipao9721=kwd-305533245293&ipao9722=351122192&ipao9723=49440702132&ipao9727=&gclid=CLiSuo-ml90CFQfQvAodvFcHLw&gclsrc=ds&dclid=CIfoyo-ml90CFQJ5vQodt0YPyA',
    ]

    def parse(self, response):
        for quote in response.css('div.cassetteitem'):
            yield {
                'house_name': quote.css('.cassetteitem_content-title::text').extract_first(),
                'address': quote.css('.cassetteitem_detail-col1::text').extract_first(),
                'transport': quote.css('.cassetteitem_detail-col2 > div.cassetteitem_detail-text::text').extract_first(),
                # 'image_urls': [quote.css('.cassetteitem_object-item > img::attr(rel)').extract_first()],
                'image_urls': ['https://s.yimg.jp/images/yjtop/promo/cm201809/topbnr_01@2x.png'],
            }

        next_page = response.css(
            '#js-leftColumnForm > div.pagination_set > div.pagination.pagination_set-nav > p > a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow('https://suumo.jp' + next_page, callback=self.parse)

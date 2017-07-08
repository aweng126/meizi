# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from meizi.items import MeiziItem


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['www.mzitu.com']

    mzi_url='http://www.mzitu.com/all/'

    def start_requests(self):
        yield Request(self.mzi_url,callback=self.parse_mziji)

    def parse_mziji(self, response):
        # print(response.text)
        mziji_url = response.css('.all ul li .url a::attr(href)').extract()
        for per_mzi_url in mziji_url:
            yield Request(per_mzi_url,self.parse_per_meiziji)

    def parse_per_meiziji(self, response):

        #真正妹子图的url
        real_mzi_url = response.css('.main .content .main-image p a img::attr(src)').extract()
        item = MeiziItem()
        item['image_urls'] = real_mzi_url
        item['name'] =response.css('.main .content .currentpath .main-title::text').extract_first()
        yield item


        #最后一个链接的提示符，如果是下一页，那么还是这个主题，所以继续添加，
        # 如果是下一组，那么跳出当前处理过程，不去继续爬取
        next = ''.join(response.css('.main .content .pagenavi a span::text').extract()[-1:])[:3]

        if '下一页'== next:
           url_next_pic = ''.join(response.css('.main .content .pagenavi a::attr(href)').extract()[-1:])
           yield Request(url_next_pic,self.parse_per_meiziji)

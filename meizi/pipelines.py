# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MeiziPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for img_url in item['image_urls']:
            yield Request(img_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item




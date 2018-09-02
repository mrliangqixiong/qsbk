# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'  # 名字是唯一的,
    allowed_domains = ['qiushibaike.com']  # 域名
    start_urls = ['https://www.qiushibaike.com/text/page/1/']  # 开始网址
    base_domain = "https://www.qiushibaike.com"

    # 解析网页
    def parse(self, response):
        duanzidivs = response.xpath("//div[@id='content-left']/div")
        # print(duanzidivs)
        for duanzidiv in duanzidivs:
            author = duanzidiv.xpath(".//h2/text()").get().strip()
            # print(author)
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()
            content = ''.join(content).strip()
            # print(content)
            item = QsbkItem(author=author, content=content)
            yield item

        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return next_url
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse)

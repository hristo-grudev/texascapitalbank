import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import TexascapitalbankItem
from itemloaders.processors import TakeFirst


class TexascapitalbankSpider(scrapy.Spider):
	name = 'texascapitalbank'
	start_urls = ['https://www.texascapitalbank.com/about-us/newsroom/press-releases',
	              'https://www.texascapitalbank.com/about-us/newsroom/latest-news']

	def parse(self, response):
		post_links = response.xpath('//a[@data-sf-field="Title"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="sf_pagerNumeric"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@data-sf-field="Title"]/text()').get()
		description = response.xpath('//div[@data-sf-field="Content"]//text()[normalize-space() and not(ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="sfnewsAuthorAndDate sfmetainfo"]/text()').get()
		date = re.findall(r'[A-Za-z]{3}\s\d{2},\s\d{4}', date)

		item = ItemLoader(item=TexascapitalbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

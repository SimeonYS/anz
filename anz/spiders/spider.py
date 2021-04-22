import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import AanzItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class AanzSpider(scrapy.Spider):
	name = 'anz'
	start_urls = ['https://media.anz.com/archive?adobe_mc=MCMID%3D54051269784940038772567130105886080562%7CMCORGID%3D67A216D751E567B20A490D4C%2540AdobeOrg%7CTS%3D1619075451']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class,"item match")]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="component article-date"]/span/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('(//div[@class="container__main__element"])[1]//text()[not (ancestor::a[@class="Transparent blue"] or ancestor::div[@class="floatingbanner"] or ancestor::div[@class="articledate"] or ancestor::div[@class="title"] or ancestor::div[@class="image"] or ancestor::script)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=AanzItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()

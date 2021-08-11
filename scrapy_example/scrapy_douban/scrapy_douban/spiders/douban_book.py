import scrapy
import bs4
from ..items import ScrapyDoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'scrapy_douban'
    allowed_domains = ['book.douban.com']
    start_urls = [f'https://book.douban.com/top250?start={i*25}' for i in range(10)]

    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        results = bs.find_all('tr', class_="item")
        for data in results:
            item = ScrapyDoubanItem()
            item['title'] = data.find_all('a')[1]['title']
            item['publish'] = data.find('p', class_='pl').text
            item['score'] = data.find('span', class_='rating_nums').text
            yield item

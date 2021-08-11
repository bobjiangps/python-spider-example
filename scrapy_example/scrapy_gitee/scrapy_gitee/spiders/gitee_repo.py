import scrapy
import bs4
from ..items import ScrapyGiteeItem


class GiteeSpider(scrapy.Spider):
    name = 'scrapy_gitee'
    allowed_domains = ['search.gitee.com']
    start_urls = [f'https://search.gitee.com/?q=crawler&type=repository&sort=stars_count&pageno={i}' for i in range(10)]

    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        results = []
        for r in bs.find_all('div', class_='item'):
            if str(r).find("更新于") >= 0:
                results.append(r)
        for data in results:
            item = ScrapyGiteeItem()
            try:
                item['title'] = data.find('a', class_='ns').text.strip()
                item['star'] = data.find('a', class_='tag stars theme-hover').text.strip()
                item['date'] = data.find_all('span', class_='tag')[-1].text
                yield item
            except Exception as e:
                continue

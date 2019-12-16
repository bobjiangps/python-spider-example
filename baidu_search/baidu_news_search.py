# -*- coding: utf-8 -*-
import sys
sys.path.append("")

from utils.http_helper import HttpHelper
from lxml import html as lh
from bs4 import BeautifulSoup as bs


if __name__ == "__main__":
    # capture the news titles recorded in baidu search

    # with lxml
    pages = 2
    keyword = "成都地铁"
    for page in range(pages+1):
        url = "https://www.baidu.com/s?tn=news&rsv_dl=ns_pc&word=%s&pn=%d" % (keyword, page*10)
        additional_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}
        response = HttpHelper.get_response_by_url(url, data=None, headers=additional_header)
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            doc = lh.fromstring(result)
            title_xpath = "//div[@class='result']/h3[@class='c-title']/a"
            nodes = doc.xpath(title_xpath)
            print("News title in page %d with the url %s: " % (page, url))
            for n in nodes:
                print(n.text_content().strip())

    # with beautifulsoap
    pages = 2
    keyword = "成都地铁"
    for page in range(pages+1):
        url = "https://www.baidu.com/s?tn=news&rsv_dl=ns_pc&word=%s&pn=%d" % (keyword, page*10)
        additional_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}
        response = HttpHelper.get_response_by_url(url, data=None, headers=additional_header)
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            bs_result = bs(result, "html.parser")
            title_h3_tag = bs_result.find_all("h3", class_="c-title")
            print("News title in page %d with the url %s: " % (page, url))
            for title in title_h3_tag:
                print(title.find("a").text.strip())

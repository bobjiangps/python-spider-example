# -*- coding: utf-8 -*-
import sys
sys.path.append("")
import os
import time

from utils.http_helper import HttpHelper
from lxml import html as lh
from urllib import parse

if __name__ == "__main__":
    additional_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}
    parent_url = True
    base_url = "https://mp.weixin.qq.com/s/6PuIEkSkaM6-FzlzB2axQQ"
    base_store_path = "./comic/weixin/download"
    crawling_pages = []
    img_errors = {}
    img_success = 0
    img_fail = 0

    if parent_url:
        response = HttpHelper.get_response_by_url(base_url, headers=additional_header, verify_ssl=False)
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            doc = lh.fromstring(result)
            title_xpath = "//h2[@class='rich_media_title']"
            title_node = doc.xpath(title_xpath)
            title_text = title_node[0].text_content().strip()
            comic_parent_path = os.path.join(base_store_path, title_text)
            if not os.path.exists(comic_parent_path):
                os.makedirs(comic_parent_path)
            base_store_path = comic_parent_path
            child_link_xpath = "//div[@class='rich_media_content ']//a[@tab='innerlink']"
            nodes = doc.xpath(child_link_xpath)
            for n in nodes:
                crawling_pages.append(n.get("href"))
        else:
            print(f"get parent page url ({base_url}) failed..")
    else:
        crawling_pages.append(base_url)

    for page in crawling_pages:
        chapter_response = HttpHelper.get_response_by_url(page, headers=additional_header, verify_ssl=False)
        if chapter_response.status_code == 200:
            chapter_result = chapter_response.content.decode('utf-8')
            chapter_doc = lh.fromstring(chapter_result)
            title_xpath = "//h2[@class='rich_media_title']"
            title_node = chapter_doc.xpath(title_xpath)
            title_text = title_node[0].text_content().strip()
            comic_chapter_path = os.path.join(base_store_path, title_text)
            if not os.path.exists(comic_chapter_path):
                os.makedirs(comic_chapter_path)
            img_xpath = "//div[@class='rich_media_content ']//img[not(contains(@class, 'bg_gif'))]"
            img_nodes = chapter_doc.xpath(img_xpath)
            for seq in range(len(img_nodes)):
                img_url = img_nodes[seq].get("data-src")
                print(f"img url is: {img_url}")
                default_img_format = "png"
                url_query_dict = parse.parse_qs(parse.urlparse(img_url).query)
                if "wx_fmt" in url_query_dict.keys():
                    default_img_format = url_query_dict["wx_fmt"][0]
                img_file_name = f"{seq}.{default_img_format}"
                img_store_path = os.path.join(comic_chapter_path, img_file_name)
                if os.path.exists(img_store_path):
                    print(f"file {img_store_path} exists, will not download again")
                else:
                    img_response = HttpHelper.get_response_by_url(img_url, headers=additional_header, verify_ssl=False)
                    if img_response.status_code == 200:
                        with open(img_store_path, "wb") as f:
                            f.write(img_response.content)
                        img_success += 1
                    else:
                        print(f"get chapter url ({img_url}) failed..")
                        img_fail += 1
                        if title_text not in img_errors.keys():
                            img_errors[title_text] = [img_url]
                        else:
                            img_errors[title_text].append(img_url)
        else:
            print(f"get page url ({page}) failed..")
        time.sleep(3)

    print(f"Download Complete...{img_success} images download successful, {img_fail} images download failed...")
    if img_fail:
        print("Please check the following urls which download failed:\n")
        for chapter in img_errors.keys():
            print(chapter)
            print(img_errors[chapter])

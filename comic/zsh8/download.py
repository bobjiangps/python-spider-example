# -*- coding: utf-8 -*-
import sys
sys.path.append("")
import os
import time

from utils.http_helper import HttpHelper
from lxml import html as lh


if __name__ == "__main__":
    additional_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}
    comic_name = "终末的后宫"
    basic_url = "https://manhua.zsh8.com/pg/zmdhfm/28155.html"
    basic_store_path = f"./comic/zsh8/download/{comic_name}"
    if not os.path.exists(basic_store_path):
        os.makedirs(basic_store_path)
    page_num = 0
    while True:
        page_num += 1
        print(f"view page {page_num}...")
        url = f"{basic_url}/page/{page_num}"
        response = HttpHelper.get_response_by_url(url, headers=additional_header, verify_ssl=False)
        # print(response.status_code)
        # with open("./temp/zsh8.html", "w") as f:
        #     f.write(response.content.decode('utf-8'))
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            doc = lh.fromstring(result)
            title_xpath = "//div[@class='fusion-builder-row fusion-row ']//div[@class='fusion-post-content post-content']/h2/a"
            nodes = doc.xpath(title_xpath)
            if len(nodes) == 0:
                print("no content, exit...")
                break
            for n in nodes:
                chapter_name = n.text_content().strip()
                chapter_url = n.get("href")
                print(chapter_name)
                print(chapter_url)
                chapter_path = os.path.join(basic_store_path, chapter_name)
                print(f"chapter path is: {chapter_path}")
                if not os.path.exists(chapter_path):
                    os.mkdir(chapter_path)
                time.sleep(3)
                chapter_response = HttpHelper.get_response_by_url(chapter_url, headers=additional_header, verify_ssl=False)
                if chapter_response.status_code == 200:
                    chapter_result = chapter_response.content.decode('utf-8')
                    chapter_doc = lh.fromstring(chapter_result)
                    img_xpath = "//div[@class='post-content']//dl[@class='gallery-item']//a"
                    img_nodes = chapter_doc.xpath(img_xpath)
                    for n in img_nodes:
                        img_url = n.get("href")
                        print(f"img url is: {img_url}")
                        img_file_name = img_url.split(os.sep)[-1]
                        img_store_path = os.path.join(basic_store_path, chapter_name, img_file_name)
                        if os.path.exists(img_store_path):
                            print(f"file {img_store_path} exists, will not download again")
                        else:
                            img_response = HttpHelper.get_response_by_url(img_url, headers=additional_header, verify_ssl=False)
                            if img_response.status_code == 200:
                                with open(img_store_path, "wb") as f:
                                    f.write(img_response.content)
                            else:
                                print(f"get chapter url ({img_url}) failed..")
                    time.sleep(3)
                else:
                    print(f"get chapter url ({chapter_url}) failed..")
        else:
            print(f"get page url ({url}) failed..")

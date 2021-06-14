# -*- coding: utf-8 -*-
import sys
sys.path.append("")
import os
import time

from utils.http_helper import HttpHelper
from lxml import html as lh


if __name__ == "__main__":
    additional_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}
    img_errors = {}
    img_success = 0
    img_fail = 0

    comic_name = "库库笔记"
    site_url = "http://www.mh857.cn"
    comic_suffix = "/index.php/comic_1560.html"
    comic_url = site_url + comic_suffix
    comic_store_path = f"./comic/mh857/download/{comic_name}"
    if not os.path.exists(comic_store_path):
        os.makedirs(comic_store_path)
    comic_response = HttpHelper.get_response_by_url(comic_url, headers=additional_header)
    if comic_response.status_code == 200:
        comic_result = comic_response.content.decode('utf-8')
        comic_doc = lh.fromstring(comic_result)
        chapter_xpath = "//ul[contains(@class, 'chapter__list-box')]//li/a"
        chapter_nodes = comic_doc.xpath(chapter_xpath)
        if len(chapter_nodes) == 0:
            print("no content, exit...")
        else:
            for cn in chapter_nodes:
                chapter_url = site_url + cn.get("href")
                chapter_name = cn.text_content().strip()
                print(chapter_name)
                print(chapter_url)
                chapter_path = os.path.join(comic_store_path, chapter_name)
                print(f"chapter path is: {chapter_path}")
                if not os.path.exists(chapter_path):
                    os.mkdir(chapter_path)
                time.sleep(3)
                chapter_response = HttpHelper.get_response_by_url(chapter_url, headers=additional_header)
                if chapter_response.status_code == 200:
                    chapter_result = chapter_response.content.decode('utf-8')
                    chapter_doc = lh.fromstring(chapter_result)
                    img_xpath = "//div[contains(@class, 'rd-article-wr')]/div[contains(@class, 'rd-article__pic')]/img"
                    img_nodes = chapter_doc.xpath(img_xpath)
                    for n in img_nodes:
                        img_url = n.get("data-original")
                        print(f"img url is: {img_url}")
                        if img_url != "http://www.mh857.cn/jpg":
                            # img_file_name = img_url.split(os.sep)[-1]
                            img_file_name = n.get("alt")
                            img_store_path = os.path.join(comic_store_path, chapter_name, img_file_name)
                            if os.path.exists(img_store_path):
                                print(f"file {img_store_path} exists, will not download again")
                            else:
                                img_response = HttpHelper.get_response_by_url(img_url, headers=additional_header)
                                if img_response.status_code == 200:
                                    with open(img_store_path, "wb") as f:
                                        f.write(img_response.content)
                                        img_success += 1
                                else:
                                    print(f"get chapter url ({img_url}) failed..")
                                    img_fail += 1
                                    if chapter_name not in img_errors.keys():
                                        img_errors[chapter_name] = [img_url]
                                    else:
                                        img_errors[chapter_name].append(img_url)
                    time.sleep(3)
                else:
                    print(f"get chapter url ({chapter_url}) failed..")
    else:
        print(f"get comic url ({comic_url}) failed..")

    print(f"Download Complete...{img_success} images download successful, {img_fail} images download failed...")
    if img_fail:
        print("Please check the following urls which download failed:\n")
        for chapter in img_errors.keys():
            print(chapter)
            print(img_errors[chapter])

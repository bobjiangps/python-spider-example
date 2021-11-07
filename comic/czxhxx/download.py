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
    not_crawler_text = ["停刊公告"]

    comic_name = "海滩女神"
    site_url = "https://czxhxx.com/"
    comic_suffix = "/manhua/714"
    comic_url = site_url + comic_suffix
    comic_store_path = f"./comic/czxhxx/download/{comic_name}"
    if not os.path.exists(comic_store_path):
        os.makedirs(comic_store_path)
    comic_response = HttpHelper.get_response_by_url(comic_url, headers=additional_header, verify_ssl=False)
    if comic_response.status_code == 200:
        comic_result = comic_response.content.decode('utf-8')
        comic_doc = lh.fromstring(comic_result)
        chapter_xpath = "//div[@id='chapterlistload']/ul/li/a"
        chapter_nodes = comic_doc.xpath(chapter_xpath)
        if len(chapter_nodes) == 0:
            print("no content, exit...")
        else:
            for cn in chapter_nodes:
                chapter_url = site_url + cn.get("href")
                chapter_name = cn.text_content().strip().replace(" ", "_").replace("…", "").replace("?", "").replace("!", "").replace("，", "")
                print(chapter_name)
                print(chapter_url)
                if chapter_name in not_crawler_text:
                    continue
                chapter_path = os.path.join(comic_store_path, chapter_name)
                print(f"chapter path is: {chapter_path}")
                if not os.path.exists(chapter_path):
                    os.mkdir(chapter_path)
                time.sleep(3)
                chapter_page_id = 0
                chapter_img_id = 0
                while True:
                    chapter_page_id += 1
                    temp_chapter_url = chapter_url + f"/?page={chapter_page_id}"
                    print(temp_chapter_url)
                    chapter_response = HttpHelper.get_response_by_url(temp_chapter_url, headers=additional_header, verify_ssl=False)
                    if chapter_response.status_code == 200:
                        chapter_result = chapter_response.content.decode('utf-8')
                        chapter_doc = lh.fromstring(chapter_result)
                        img_xpath = "//div[@class='comicpage']/div/img"
                        img_nodes = chapter_doc.xpath(img_xpath)
                        for n in img_nodes:
                            chapter_img_id += 1
                            img_url = n.get("data-original")
                            print(f"img url is: {img_url}")
                            img_file_name = img_url.split(os.sep)[-1]
                            img_suffix = img_file_name.split(".")[-1]
                            img_store_path = os.path.join(comic_store_path, chapter_name, f"{chapter_img_id}.{img_suffix}")
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
                        next_xpath = "//a[@id='nextPage']"
                        next_page_nodes = chapter_doc.xpath(next_xpath)
                        if len(next_page_nodes) == 0:
                            break
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


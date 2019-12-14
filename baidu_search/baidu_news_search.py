# -*- coding: utf-8 -*-
import sys
sys.path.append("")

from utils.http_helper import HttpHelper


if __name__ == "__main__":
    url = "https://www.baidu.com/s?tn=news&rsv_dl=ns_pc&word=成都地铁"
    additional_header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}
    r = HttpHelper.get_response_by_url(url, data=None, headers=additional_header)
    print(r.content)
    print(r.status_code)
    with open("./baidu_news.html", "w") as f:
        f.write(r.content.decode('utf-8'))
    # debug, incomplete

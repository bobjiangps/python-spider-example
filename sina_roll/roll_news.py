import sys
sys.path.append("")
import json
from utils.http_helper import HttpHelper


if __name__ == "__main__":
    # https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1
    url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1&r=0.27076940029916763&callback=jQuery111208748664832668509_1628588203409&_=1628588203412"
    additional_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    response = HttpHelper.execute("get", url, headers=additional_header)
    if response.status_code == 200:
        results = json.loads(response.text[46:-14])
        for i in range(50):
            print(results['result']['data'][i]['title'])
            print(results['result']['data'][i]['url'])

import requests


if __name__ == "__main__":
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0',
        'Connection': 'keep-alive',
        'cookie': 'replace your cookie here' # update text
    }

    session = requests.Session()
    response = session.get('https://weibo.com/2671109275/fans?rightmod=1&wvr=6', headers=headers)
    print(response.text)
    print(response.status_code)
import sys
sys.path.append("")
import re
import requests
from urllib import parse


class Github:

    def __init__(self, email, pw):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Referer": "https://github.com/",
            "Host": "github.com"
        }
        self.email = email
        self.pw = pw
        self.token = None
        self.username = None
        self.base_url = "https://github.com"
        self.session = requests.session()

    def login(self):
        page_response = self.session.get(parse.urljoin(self.base_url, "login"), headers=self.headers)
        if page_response.status_code == 200:
            token_match = re.search('name="authenticity_token" value="(.*?)"', page_response.text)
            self.token = token_match.group(1)
        else:
            print("retrieve login url fail")

        sign_in_data = {
            "commit": "Sign in",
            "authenticity_token": self.token,
            "login": self.email,
            "password": self.pw
        }
        sign_in_response = self.session.post(parse.urljoin(self.base_url, "session"), data=sign_in_data, headers=self.headers)
        if sign_in_response.status_code == 200:
            self.username = re.search(r'"user-login" content="(.*?)"', sign_in_response.text).group(1)
            r = self.session.get("https://github.com/settings/profile")
            if r.text.find("Save jobs profile"):
                print("sign in successfully")
        else:
            print("sign in failed")
        return self.session

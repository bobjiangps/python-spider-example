import sys
sys.path.append("")
from gh.github import Github
from getpass import getpass
from lxml import html as lh


class MyGithub(Github):

    def search(self, keyword):
        self.login()
        print(f"--search in github after login with keyword: {keyword}--")
        response = self.session.get(f"{self.base_url}/search?q={keyword}", headers=self.headers)
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            doc = lh.fromstring(result)
            title_xpath = "//ul[@class='repo-list']/li//a[@class='v-align-middle']"
            nodes = doc.xpath(title_xpath)
            for n in nodes:
                print(n.text_content().strip())


if __name__ == "__main__":
    email = getpass("email:")
    password = getpass("Password:")
    MyGithub(email, password).search("automation")

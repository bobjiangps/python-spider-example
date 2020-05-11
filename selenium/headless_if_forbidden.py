from selenium import webdriver
from selenium.webdriver.firefox.options import Options

firefox_options = Options()
firefox_options.set_headless()
firefox_options.add_argument('--disable-gpu')
driver = webdriver.Firefox(firefox_options=firefox_options)
driver.get("https://haveibeenpwned.com/")
html = driver.page_source
print(html)
driver.quit()

############################################
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Connection': 'keep-alive'
}

cap = DesiredCapabilities.PHANTOMJS.copy()
for key, value in headers.items():
    cap['phantomjs.page.customHeaders.{}'.format(key)] = value
driver = webdriver.PhantomJS("./phantomjs", desired_capabilities=cap)

driver.get("https://haveibeenpwned.com/")
html = driver.page_source
print(html)
driver.quit()

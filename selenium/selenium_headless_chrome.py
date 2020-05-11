from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# with headless Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://news.163.com/rank/")
article_title_elements = driver.find_elements(By.XPATH, "//div[@class='area areabg1']/div[2]//div[@class='tabContents active']//td[@class='red']/a")
article_view_elements = driver.find_elements(By.XPATH, "//div[@class='area areabg1']/div[2]//div[@class='tabContents active']//td[@class='red']/following-sibling::td")
for seq in range(len(article_title_elements)):
    print(article_title_elements[seq].text)
    print(article_view_elements[seq].text)
# html = driver.page_source
# print(html)
driver.quit()

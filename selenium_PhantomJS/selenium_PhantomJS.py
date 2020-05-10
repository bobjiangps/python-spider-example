from selenium import webdriver
from selenium.webdriver.common.by import By


keyword = 18180849516
driver = webdriver.PhantomJS("./phantomjs")
driver.get(f'https://www.reg007.com/search?q={keyword}')
name_elements = driver.find_elements(By.XPATH, "//ul[@id='site_list']//li[contains(@id, 'li_') and @data-category]//h4[@class='media-heading']/a")
desc_elements = driver.find_elements(By.XPATH, "//ul[@id='site_list']//li[contains(@id, 'li_') and @data-category]//p[@class='site-desc']")
for seq in range(len(name_elements)):
    print(name_elements[seq].text)
    print(desc_elements[seq].text)
# html = driver.page_source
# print(html)
driver.quit()
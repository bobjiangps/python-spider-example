from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import getpass


class CustomizedWait(WebDriverWait):
    def wait_until_presence_of_element(self, by, value):
        return self.until(EC.presence_of_element_located((by, value)), "fail to wait until presence")

    def wait_until_visibility_of_element(self, by, value):
        return self.until(EC.visibility_of_element_located((by, value)), "fail to wait until visibility")


def login(dr, name, pwd):
    user_input = dr.find_element(By.ID, "loginname")
    pwd_input = dr.find_element(By.NAME, "password")
    login_button = dr.find_element(By.XPATH, "//div[@class='info_list login_btn']/a")
    user_input.send_keys(name)
    pwd_input.send_keys(pwd)
    login_button.click()


if __name__ == "__main__":
    user_name = input("input user name:\n")
    password = getpass.getpass("input password:\n")
    url = "https://weibo.com/"
    driver = webdriver.Chrome()
    driver.get(url)
    cw = CustomizedWait(driver, 30)
    cw.wait_until_presence_of_element("id", "loginname")
    login(driver, user_name, password)
    cw.wait_until_presence_of_element("xpath", "//ul[@class='gn_nav_list']//a[@class='gn_name']")
    driver.quit()
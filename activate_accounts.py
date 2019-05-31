import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from utils.basic import Basic
from utils import config


class Activate(Basic):
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)
    driver.get("https://myaccount.google.com/")

    def login_to_gmail(self, email, password):
        self.driver.get("https://gmail.com")
        self.click_el()




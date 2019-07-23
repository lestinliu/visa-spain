import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from visa import Visa
from utils import config

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(1)

visa = Visa(driver)

visa.update_emails()

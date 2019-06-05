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


def go_to_select_date_page():
    visa.open_page("https://blsspain-belarus.com/book_appointment.php")
    visa.select_centre("Minsk", "Normal")
    visa.enter_phone_and_email(config.PHONE, config.EMAIL)
    visa.enter_wrong_code(config.EMAIL, config.PASSWORD)
    visa.enter_code_from_email(config.EMAIL)  # b


def monitor_dates(timeout):
    try:
        while True:
            visa.write_available_dates(visa.wait_for_available_dates())
            time.sleep(timeout)
            driver.refresh()
    except:
        go_to_select_date_page()
        monitor_dates(timeout)

monitor_dates(config.TIMEOUT)

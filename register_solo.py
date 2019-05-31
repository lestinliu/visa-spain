import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from visa import Visa
from utils import config

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(1)

visa = Visa(driver)


def go_to_select_date_page():
    visa.fill_emails()
    visa.open_page("https://blsspain-belarus.com/book_appointment.php")
    visa.select_centre("Minsk", "Normal")
    visa.enter_phone_and_email(config.PHONE, config.EMAIL)
    visa.enter_wrong_code()
    visa.enter_code_from_email(config.EMAIL)  # Иногда приходит письмо с security alert и не читается код


def register_people(timeout):
    try:
        while True:
            visa.register_people_for_dates(visa.wait_for_available_dates())
    except:
        go_to_select_date_page()
        register_people(timeout)


go_to_select_date_page()
register_people(config.TIMEOUT)

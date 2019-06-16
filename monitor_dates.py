import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from visa import Visa
from utils import config
import telebot

bot = telebot.TeleBot('803883229:AAHGFPQ1guQEZylgE0_IdErXrkUpfolhT-c')
options = Options()
#options.add_argument('--headless')
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
        go_to_select_date_page()
        while True:
            dates = visa.get_available_dates()
            people = visa.get_available_people()
            available_dates = visa.collect_people_for_dates(dates, people)
            if not available_dates:
                visa.send_monitoring_message(bot, "🔍 No dates. Monitoring...")
                time.sleep(timeout)
                driver.refresh()
            else:
                visa.send_monitoring_message(bot, "😃 Ready to register: {}".format(available_dates.keys()))
    except Exception as e:
        visa.send_monitoring_message(bot, "❌ Monitor dates error: {}".format(str(e)))
        time.sleep(timeout)
        monitor_dates(timeout)


visa.send_monitoring_message(bot, "Checking available dates for people in spreadsheet ...")
monitor_dates(config.TIMEOUT)

from datetime import datetime
import json
import time

import telebot
from selenium import webdriver
from visa import Visa
from utils import config

bot = telebot.TeleBot('803883229:AAHGFPQ1guQEZylgE0_IdErXrkUpfolhT-c')

appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local"
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}

profile = {"printing.print_preview_sticky_settings.appState": json.dumps(appState),
           'savefile.default_directory': "/Users/a.kardash/Drive",
           "download.prompt_for_download": False,
           "profile.default_content_setting_values.notifications": 2}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', profile)
chrome_options.add_argument('--kiosk-printing')
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(1)

visa = Visa(driver)


def go_to_select_date_page():
    visa.open_page("https://blsspain-belarus.com/book_appointment.php")
    visa.select_centre("Minsk", "Normal")
    visa.enter_phone_and_email(config.PHONE, config.EMAIL)
    visa.enter_wrong_code(config.EMAIL, config.PASSWORD)
    visa.enter_code_from_email(config.EMAIL)


def register_people(timeout):
    try:
        while True:
            available_dates = visa.read_available_dates()
            if available_dates:
                for date in available_dates:
                    for person in available_dates[date]:
                        visa.go_to_select_date_page(person["phone"], person["email"])
                        visa.send_register_message(
                            bot, visa.register_person_for_date(person, datetime.strptime(date, "%d/%m/%Y")))
            else:
                visa.send_register_message(
                    bot, "🔍 No dates. Waiting...")
                time.sleep(timeout)
                driver.refresh()
    except Exception as e:
        visa.send_register_message(bot, "❌ Register people error: {}".format(str(e)))
        register_people(timeout)

register_people(config.TIMEOUT)

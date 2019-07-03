import json
import time
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from visa import Visa
from utils import config
import telebot

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
           'savefile.default_directory': "/Users/Shared/Drive/visa",
           "download.prompt_for_download": False,
           "profile.default_content_setting_values.notifications": 2}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', profile)
chrome_options.add_argument('--kiosk-printing')
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(5)
visa = Visa(driver)


def go_to_select_date_page():
    visa.open_page("https://blsspain-belarus.com/book_appointment.php")
    visa.select_centre("Minsk", "Normal")
    visa.enter_phone_and_email(config.PHONE, config.EMAIL)
    visa.enter_wrong_code(config.EMAIL, config.PASSWORD)
    visa.enter_code_from_email(config.EMAIL)  # b


def monitor_dates(timeout):
    go_to_select_date_page()
    try:
        while True:
            dates = visa.get_available_dates()
            str_dates = "😃 Available dates found:\n"
            for date in dates:
                str_dates += date + "; "
            visa.send_monitoring_message(bot, str_dates)
            people = visa.get_available_people()
            available_dates = visa.collect_people_for_dates(dates, people)
            with open('resources/dates.json', 'w') as fp:
                json.dump(available_dates, fp)
            if not available_dates:
                time.sleep(timeout)
                driver.refresh()
            else:
                people_found = "😃 Ready to register:\n"
                for k, v in available_dates.items():
                    for person in v:
                        people_found += "{}: {} - {}\n".format(k, person["id"], person["passport"])
                visa.send_monitoring_message(bot, people_found)
                register_people(available_dates)
                time.sleep(timeout)
                driver.back()
                driver.refresh()
    except Exception as e:
        print("Monitor error: {}".format(str(e)))
        monitor_dates(timeout)


def register_people(available_dates):
    error_message = ""
    for date in available_dates:
        try:
            for person in available_dates[date]:
                visa.go_to_select_date_page(person["phone"], person["email"])
                # need to delete date from dates.json
                visa.send_register_message(
                    bot, visa.register_person_for_date(person, datetime.strptime(date, "%d/%m/%Y")))
        except Exception as e:
            error_message += str(e)
    if error_message:
        visa.send_register_message(bot, "Register errors: {}".format(error_message))


visa.send_monitoring_message(bot, "Checking available dates for people in spreadsheet ...")
monitor_dates(config.TIMEOUT)

import json
import subprocess
import time
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from visa import Visa
from utils import config
import telebot

bot = telebot.TeleBot('1275523107:AAF_5t_r80J55Pl-JcVeLcVVOsl7kadqAc4')

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
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)
visa = Visa(driver)


def monitor_dates(timeout):
    # visa.disable_vpn()
    visa.update_emails()
    visa.go_to_select_date_page(config.PHONE, config.EMAIL)
    try:
        while True:
            dates = visa.get_available_dates()
            bot.send_photo(chat_id=config.CHAT_ID, photo=driver.get_screenshot_as_png(), caption=f'dates: {dates}')
            visa.fill_emails()
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
                subprocess.call("/usr/local/bin/python3.9 create_links.py", shell=True)
                time.sleep(timeout)
                driver.back()
                driver.refresh()
    except Exception as e:
        print("Monitor error: {}".format(str(e)))
        monitor_dates(timeout)


def register_people(available_dates):
    success_message = ""
    error_message = ""
    for date in available_dates:
        try:
            for person in available_dates[date]:
                visa.go_to_select_date_page(person["phone"], person["email"])
                success_message += visa.register_person_for_date(person, datetime.strptime(date, "%d/%m/%Y"))
        except Exception as e:
            error_message += str(e)
    time.sleep(60) # time for bot to recover after vpn change
    visa.send_register_message(bot, success_message)
    if error_message:
        visa.send_register_message(bot, "Register errors: {}".format(error_message))


visa.send_monitoring_message(bot, "Checking available dates for people in spreadsheet ...")
monitor_dates(config.TIMEOUT)

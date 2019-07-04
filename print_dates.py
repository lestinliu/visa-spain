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


def get_dates():
    try:
        visa.go_to_select_date_page(config.PHONE, config.EMAIL)
        dates = visa.get_available_dates()
        if dates:
            str_dates = "😃 Достыпные даты:\n"
            month = ""
            for date in dates:
                d = datetime.strptime(date, "%d/%m/%Y")
                if d.month != month:
                    month = d.month
                    str_dates += "\n[{}]: ".format(month)
                str_dates += str(d.day) + ", "
        else:
            str_dates = "❌ Нет дат"
        bot.send_message(-1001497020962, str_dates)
    except Exception as e:
        bot.send_message(-1001497020962, "Ошибка: {}".format(str(e)))

get_dates()
driver.quit()

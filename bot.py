import subprocess
import time

import telebot
from requests.packages.urllib3.exceptions import ReadTimeoutError
from telebot.apihelper import ApiException

last_message = ""
bot = telebot.TeleBot('803883229:AAHGFPQ1guQEZylgE0_IdErXrkUpfolhT-c')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Motitoring dates and people...')
    try:
        subprocess.call("pkill -f" + " monitor_dates.py", shell=True)
    except:
        pass
    finally:
        subprocess.call("/usr/local/bin/python3.7 monitor_dates.py", shell=True)


@bot.message_handler(commands=['stop'])
def start_message(message):
    bot.send_message(message.chat.id, 'Motitoring stopped...')
    subprocess.call("pkill -f" + " monitor_dates.py", shell=True)


@bot.message_handler(commands=['dates'])
def start_message(message):
    try:
        subprocess.call("pkill -f" + " print_dates.py", shell=True)
    except:
        pass
    finally:
        subprocess.call("/usr/local/bin/python3.7 print_dates.py", shell=True)


@bot.message_handler(commands=['links'])
def start_message(message):
    try:
        subprocess.call("pkill -f" + " create_links.py", shell=True)
    except:
        pass
    finally:
        subprocess.call("/usr/local/bin/python3.7 create_links.py", shell=True)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)

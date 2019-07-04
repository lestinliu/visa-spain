import subprocess

import telebot
from utils import config

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
    subprocess.call("pkill -f" + " register_solo.py", shell=True)


@bot.message_handler(commands=['dates'])
def start_message(message):
    print("id: {}".format(message.chat.id))
    try:
        subprocess.call("pkill -f" + " print_dates.py", shell=True)
    except:
        pass
    finally:
        subprocess.call("/usr/local/bin/python3.7 print_dates.py", shell=True)



@bot.message_handler(commands=['register'])
def start_message(message):
    bot.send_message(message.chat.id, 'Registering people...')
    try:
        subprocess.call("pkill -f" + " register_solo.py", shell=True)
    except:
        pass
    finally:
        subprocess.call("/usr/local/bin/python3.7 register_solo.py", shell=True)


bot.polling()

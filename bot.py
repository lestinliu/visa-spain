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

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if "timeout " in message.text:
        config.TIMEOUT = int(message.split()[1])
        bot.send_message(message.from_user.id, "Timeout is changed to {}".format(int(message.split()[1])))
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Available commands:\n"
                                               "/start - to start monitoring dates\n"
                                               "/stop - to stop all proceses\n"
                                               "/register - to register available people\n"
                                               "timeout sec - to change retry timeout")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling()

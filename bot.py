import subprocess

import telebot

last_message = ""
bot = telebot.TeleBot('803883229:AAHGFPQ1guQEZylgE0_IdErXrkUpfolhT-c')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Available commands:')
    bot.send_message(message.chat.id, '/start motinoring')
    bot.send_message(message.chat.id, '/stop all')
    bot.send_message(message.chat.id, '/register available people')
    print("{}".format(message.chat.id))

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

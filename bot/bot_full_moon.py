# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem

import settings


import logging

logging.basicConfig(format=('%(name)s - %(levelname)s - %(message)s'), level=logging.INFO, filename='bot_full_moon.log')


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('moon', next_full_moon, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update, user_data):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(bot, update, user_data):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


# Полнолуние
def next_full_moon(bot, update, user_data):
    command = update.message.text
    moon = command.split()[-1]
    print(moon)
    date = moon[:-1] if '?' in moon else moon
    print(date)
    full_moon = ephem.next_full_moon(date)
    update.message.reply_text(full_moon)


# Вызываем функцию - эта строчка собственно запускает бота
main()

# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings


import logging

logging.basicConfig(format=('%(name)s - %(levelname)s - %(message)s'), level=logging.INFO, filename='bot_wordcount.log')


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('wordcount', wordcount, pass_user_data=True))
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


# Подсчёт количества слов
def wordcount(bot, update, user_data):
    command = update.message.text
    word = command.split()
    if len(word) == 1:
        update.message.reply_text('InvalidCommand')
        return
    if '""' in word:
        update.message.reply_text('NoneString')
        return
    count = len(word) - 1
    update.message.reply_text('%.i слова' % count)


# Вызываем функцию - эта строчка собственно запускает бота
main()

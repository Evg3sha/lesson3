# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings


import logging

logging.basicConfig(format=('%(name)s - %(levelname)s - %(message)s'), level=logging.INFO, filename='bot_calculate.log')


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('calculator1', calculator1, pass_user_data=True))
    dp.add_handler(CommandHandler('calculator2', calculator2, pass_user_data=True))
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


# Бот- словарный калькулятор
def calculate(list):
    arr1 = list[0]
    arr2 = list[1]
    arr3 = list[2]
    if arr2 == '+':
        result1 = int(arr1) + int(arr3)
        return result1
    elif arr2 == '-':
        result2 = int(arr1) - int(arr3)
        return result2
    elif arr2 == '*':
        result3 = int(arr1) * int(arr3)
        return result3
    elif arr2 == '/':
        if int(arr3) == 0:
            return None
        else:
            result4 = int(arr1) / int(arr3)
            return result4


# Бот- калькулятор
def calculator1(bot, update, user_data):
    command = update.message.text
    expr = command.split()[1]
    result = calculate(expr)
    if result is None:
        update.message.reply_text('DivisionByZero')
    else:
        update.message.reply_text(result)


def calculator2(bot, update, user_data):
    command = update.message.text
    chisla = {'один': '1', 'два': '2', 'три': '3', 'четыре': '4', 'пять': '5', 'шесть': '6', 'семь': '7', 'восемь': '8',
              'девять': '9', 'плюс': '+', 'минус': '-', 'равно': '='}
    command = command.replace("'", '')
    words = command.split()[1:]
    new = []
    for i in words:
        new += chisla[i]
    result = calculate(new)
    if result is None:
        update.message.reply_text('DivisionByZero')
    else:
        update.message.reply_text(result)


# Вызываем функцию - эта строчка собственно запускает бота
main()

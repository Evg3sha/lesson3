# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
from random import choice
from emoji import emojize
import settings


import logging

logging.basicConfig(format=('%(name)s - %(levelname)s - %(message)s'), level=logging.INFO, filename='bot3.log')

list_of_cities = ['Москва', 'Адлер', 'Екатеринбург', 'Реутов', 'Волгоград', 'Домодедово', 'Облучье']


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', planet, pass_user_data=True))
    dp.add_handler(CommandHandler('solve_quadratic', solve_quadratic, pass_user_data=True))
    dp.add_handler(CommandHandler('wordcount', wordcount, pass_user_data=True))
    dp.add_handler(CommandHandler('calculator1', calculator1, pass_user_data=True))
    dp.add_handler(CommandHandler('calculator2', calculator2, pass_user_data=True))
    dp.add_handler(CommandHandler('moon', next_full_moon, pass_user_data=True))
    dp.add_handler(CommandHandler('goroda', goroda, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет {}'.format(emo)
    update.message.reply_text(text)


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = 'Привет {} {}! Ты написал: {}'.format(update.message.chat.first_name, emo,
                                                      update.message.text)
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def create_planet_obj(name):
    function = getattr(ephem, name, None)
    if function is None:
        return None
    return function()


# созвездия
def planet(bot, update, user_data):
    command = update.message.text
    planets = command.split()
    if len(planets) != 2:
        update.message.reply_text('InvalidCommand')
        return
    planet_name = planets[1]
    planet = create_planet_obj(planet_name)
    if planet is None:
        update.message.reply_text('InvalidPlanetName')
        return
    planet.compute()
    const = ephem.constellation(planet)
    update.message.reply_text('Planet ' + planet_name + ' is in constellation ' + const[1])


# квадратное уравнение
def solve_quadratic(bot, update, user_data):
    command = update.message.text
    quadratic = command.split()
    if len(quadratic) != 4:
        update.message.reply_text('InvalidCommand')
        return
    a = int(quadratic[1])
    b = int(quadratic[2])
    c = int(quadratic[3])
    discr = b ** 2 - 4 * a * c
    if discr > 0:
        import math
        x1 = (-b + math.sqrt(discr)) / (2 * a)
        x2 = (-b - math.sqrt(discr)) / (2 * a)
        update.message.reply_text("x1 = %.2f \nx2 = %.2f" % (x1, x2))
    elif discr == 0:
        x = -b / (2 * a)
        update.message.reply_text("x = %.2f" % x)
    else:
        update.message.reply_text("Корней нет")


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


# Полнолуние
def next_full_moon(bot, update, user_data):
    command = update.message.text
    moon = command.split()[-1]
    print(moon)
    date = moon[:-1] if '?' in moon else moon
    print(date)
    full_moon = ephem.next_full_moon(date)
    update.message.reply_text(full_moon)


last_letter = ''


# Города
def goroda(bot, update, user_data):
    global last_letter
    command = update.message.text
    word = command.split()[1]
    first_letter = word[-1]
    print(first_letter)

    if last_letter != '':
        if word[0].upper() != last_letter.upper():
            update.message.reply_text("Эй, чувак, не та буква")
            return
    if word in list_of_cities:
        list_of_cities.remove(word)
    else:
        update.message.reply_text("Эй, чувак, нет города в списке")
        return

    for i in list_of_cities:
        if first_letter.upper() == i[0].upper():
            update.message.reply_text('{}, ваш ход.'.format(i))
            last_letter = i[-1]
            list_of_cities.remove(i)

    print(list_of_cities)


# Вызываем функцию - эта строчка собственно запускает бота
main()

# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings


import logging

logging.basicConfig(format=('%(name)s - %(levelname)s - %(message)s'), level=logging.INFO, filename='bot_goroda.log')



list_of_cities = ['Москва', 'Адлер', 'Екатеринбург', 'Реутов', 'Волгоград', 'Домодедово', 'Облучье']


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('goroda', goroda, pass_user_data=True))
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

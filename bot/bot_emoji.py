# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import choice
from emoji import emojize
import settings

import logging

logging.basicConfig(format=('%(name)s - %(levelname)s - %(message)s'), level=logging.INFO, filename='bot_emoji.log')


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
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


# Вызываем функцию - эта строчка собственно запускает бота
main()

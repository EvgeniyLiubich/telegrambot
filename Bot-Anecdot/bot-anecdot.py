from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from settings import TG_TOKEN, TG_API_URL, WEATHER_KEY
from bs4 import BeautifulSoup
import requests
from parse_kinopoisk import get_random_film


def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?')
    bot.message.reply_text('Привет {}, я бот! \nПоговори со мной!'.format(bot.message.chat.first_name),
                           reply_markup=get_keyboard())

    # print(bot.message)


def get_weather(bot, update):
    query = 'Минск'
    params = {
        'access_key': WEATHER_KEY,
        'query': query
    }
    r = requests.get('http://api.weatherstack.com/current', params)
    if 'current' in r.json():
        text_response = f"Сейчас в {query}е {r.json()['current']['temperature']} градус(-а, -ов)"
        bot.message.reply_text(text_response)
    elif 'current' not in r.json():
        print('Ключа "current" нет')


def get_film(bot, update):
    text_response = get_random_film()
    print(text_response[0])
    # bot.message.reply_text(text_response[0])
    bot.message.reply_text(text_response[1])


def get_anecdote(bot, update):
    r = requests.get('http://anekdotme.ru/random')
    page = BeautifulSoup(r.text, 'html.parser')
    find = page.select(".anekdot_text")
    print(find)
    for text in find:
        page = (text.getText().strip())
    bot.message.reply_text(page)


def parrot(bot, update):
    print(bot.message.text)
    bot.message.reply_text(bot.message.text)


def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Начать', 'Анекдот'], ['Погода в столице', 'Случайный фильм'],
                                       [contact_button, location_button]], resize_keyboard=True)
    return my_keyboard


def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Погода в столице'), get_weather))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Случайный фильм'), get_film))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()


main()

import telebot
from constants import *
from func import *
bot = telebot.TeleBot(TG_TOKEN)
@bot.message_handler(commands=['start', 'help'])
def msg(message):
    start_help(message)

@bot.message_handler(commands=['dict'])
def msg(message):
    dictionary(message)

@bot.message_handler(commands=['tiktokdl'])
def msg(message):
    tiktok_dl(message)

@bot.message_handler(commands=['qr'])
def msg(message):
    generate_qr(message)

@bot.message_handler(commands=['apod'])
def apod(message):
    apodimg(message)

@bot.message_handler(commands=['ufacts'])
def msg(message):
    uselessf(message)

@bot.message_handler(commands=['smovie'])
def msg(message):
    s_movie(message)

@bot.message_handler(commands=['horoscope'])
def msg(message):
    getHoroscope(message)
bot.polling()

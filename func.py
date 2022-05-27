from ast import excepthandler
import telebot
import json
import requests
from constants import *
import pyaztro
bot = telebot.TeleBot(TG_TOKEN)

github = '[Github](https://github.com/sudo-paoo/telegram_bot)'

def start_help(message):
    bot.send_message(message.chat.id, text=f"""
Hi, I am 🛠_FLUX TELEGRAM BOT_🛠
Here are my commands
/start or /help
📖Provide an overview of my commands
/apod
📖Provides the Astronomy Picture of the Day <YYYY-MM-DD> format
Example: /apod <YYYY-MM-DD>
/dict 
📖Provide the part of speech and definition of the word
Example: /dict <word>
/horoscope
📖Provide the horoscope of your sign
Example: /horoscope gemini
/qr 
📖Generates a qr code
Example: /qr <text you want to put in the qr code>
/smovie
📖Provide the title, year, released date, director, plot, ratings, etc. of the movie
Example: /smovie <title>
/tiktokdl
📖Downloads a tiktok video without watermark
Example: /tiktokdl <link>
/ufacts
📖Send useless facts
*Made By:* @sudopao
*Language:* _Python_ 
*Framework:* _Telebot_
*Github Repository: {github}*""", parse_mode='MarkdownV2')

def dictionary(message):
    user_message = message.text
    msg = user_message.split(' ')
    if len(msg) != 1:
        try:
            word = msg[1]
            botmsg = bot.send_message(message.chat.id, 'Finding the word in the dictionary')
            resp = requests.get(DICT_URL + word)
            respData = resp.json()
            pof = respData[0]['meanings'][0]['partOfSpeech']
            print(pof)
            defi = respData[0]['meanings'][0]['definitions'][0]['definition']
            print(defi)
            bot.send_message(message.chat.id, text=f'*Word:* {word} \n\n *Part Of Speech: *{pof} \n\n *Definition: *{defi}', parse_mode='MarkdownV2')
            bot.delete_message(message.chat.id, botmsg.message_id)
        except:
            bot.send_message(message.chat.id, "Couldn't find in the dictionary.")
    else:
        bot.send_message(message.chat.id, 'Please input a word to define.')

def tiktok_dl(message):
    user_message = message.text
    msg_split = user_message.split(' ')
    if len(msg_split) != 1:
        try:
            bot_msg = bot.send_message(message.chat.id, 'Downloading TikTok Video.')
            link = msg_split[1]
            resp = requests.get(TIKTOK_URL + link)
            respData = json.loads(resp.text)
            bot.send_chat_action(message.chat.id, action='upload_video')
            bot.send_video(message.chat.id, video=respData['no_watermark'], caption='*Downloaded By: *@FluxAllAroundBot', parse_mode='MarkdownV2')
            bot.delete_message(message.chat.id, bot_msg.message_id)
        except:
            bot.send_message(message.chat.id, 'Sorry, something went wrong. Please try again')
            bot.delete_message(message.chat.id, bot_msg.message_id)
    else:
        bot.send_message(message.chat.id, 'Please input tiktok link to download')

def generate_qr(message):
    user_message = message.text
    qr_data = user_message.split(' ', 1)
    if len(qr_data) != 1:
        try:
            bot_msg = bot.send_message(message.chat.id, 'Generating QR Code.')
            qr = QR_URL + qr_data[1]
            bot.send_chat_action(message.chat.id, action='upload_photo')
            bot.send_photo(message.chat.id, photo=qr)
            bot.delete_message(message.chat.id, bot_msg.message_id)
        except:
            bot.send_message(message.chat.id, 'Sorry there was an error generating QR Code. Please try again.')
            bot.delete_message(message.chat.id, bot_msg.message_id)
    else:
        bot.send_message(message.chat.id, 'Please input a statement/paragraph to generate qr code.')

def apodimg(message):
    user_message = message.text
    split_msg = user_message.split(' ')
    if len(split_msg) != 1:
        try:
            bot_msg = bot.send_message(message.chat.id, 'Gathering data from NASA.')
            date = split_msg[1]
            params = {
            'api_key': NASA_API,
            'hd': 'True',
            'date': date
            }
            resp = requests.get(NASA_URL + NASA_API, params=params)
            respData = json.loads(resp.text)
            date = respData['date']
            title = respData['title']
            explanation = respData['explanation']
            bot.send_chat_action(message.chat.id, action='upload_photo')
            bot.send_photo(message.chat.id, photo=respData['hdurl'], caption=f'*Title: *  {title} \n\n *Date: * {date} \n\n *Description: * {explanation}', parse_mode='MarkdownV2')
            bot.delete_message(message.chat.id, bot_msg.message_id)
        except KeyError:
            bot.send_message(message.chat.id, 'There was and error finding the image with the given date. Please try again.')
            bot.delete_message(message.chat.id, bot_msg.message_id)
        except:
            bot_msg_new = bot.send_message(message.chat.id, 'There is a problem with the first image url. Sending the second image url. Please wait')
            date = split_msg[1]
            params = {
            'api_key': NASA_API,
            'hd': 'True',
            'date': date
            }
            resp = requests.get(NASA_URL + NASA_API, params=params)
            respData = json.loads(resp.text)
            date = respData['date']
            title = respData['title']
            explanation = respData['explanation']
            bot.send_chat_action(message.chat.id, action='upload_photo')
            bot.send_photo(message.chat.id, photo=respData['url'], caption=f'*Title: *  {title} \n\n *Date: * {date} \n\n *Description: * {explanation}', parse_mode='MarkdownV2')
            bot.delete_message(message.chat.id, bot_msg.message_id)
    else:
        bot.send_message(message.chat.id, 'Please input a valid date.')

def uselessf(message):
    uf = requests.get(U_FACTS)
    data = json.loads(uf.text)
    bot.send_message(message.chat.id, text='*Useless Fact:* \n\n' + data['text'], parse_mode='MarkdownV2')

def s_movie(message):
    bot_msg = bot.send_message(message.chat.id, 'Gathering Movie Information.')
    msg = message.text
    title = msg[msg.find(' '):].strip()
    if len(title) != 1:
        try:
            movie = requests.get(MOVIE_URL_API + title)
            movie_data = json.loads(movie.text)
            mTitle = movie_data['Title']
            mYear = movie_data['Year']
            mRated = movie_data['Rated']
            mReleased = movie_data['Released']
            mRuntime = movie_data['Runtime']
            mGenre = movie_data['Genre']
            mDirector = movie_data['Director']
            mWriter = movie_data['Writer']
            mPlot = movie_data['Plot']
            mLanguage = movie_data['Language']
            mCountry = movie_data['Country']
            mAwards = movie_data['Awards']
            mRatingS = movie_data['Ratings'][0]['Source']
            mRatingV = movie_data['Ratings'][0]['Value']
            mPoster = movie_data['Poster']
            bot.send_photo(message.chat.id, photo=mPoster, caption=f'*Title: * {mTitle} \n\n *Year: * {mYear} \n\n *Rated: * {mRated} \n\n *Released: * {mReleased} \n\n *Runtime: * {mRuntime} \n\n *Genre: * {mGenre} \n\n *Director/s: * {mDirector} \n\n *Writer/s: * {mWriter} \n\n *Plot: * {mPlot} \n\n *Language: * {mLanguage} \n\n *Country: * {mCountry} \n\n *Award/s: * {mAwards} \n\n *Rating By: * {mRatingS} \n\n *Rating: * {mRatingV}', parse_mode='MarkdownV2')
            bot.delete_message(message.chat.id, bot_msg.message_id)
        except:
            bot.send_message(message.chat.id, 'There was an error finding the movie you were looking for. Please try again.')
    else:
        bot.send_message(message.chat.id, 'Please input a movie title.')

def getHoroscope(message):
    split = message.text.split(' ')
    if len(split) != 1:
        try:
            sign = split[1]
            hs = pyaztro.Aztro(sign=sign.lower())
            mood = hs.mood
            lTime = hs.lucky_time
            description = hs.description
            color = hs.color
            compa = hs.compatibility
            lNum = hs.lucky_number
            date = hs.current_date
            bot.send_message(message.chat.id, text=f'Sign: {sign.capitalize()} \n\nDate: {date}\n\nMood: {mood} \n\nLucky Time: {lTime} \n\nDescription: {description} \n\nColor: {color} \n\nSign Compatibility: {compa} \n\nLucky Number: {lNum}')
        except:
            bot.send_message(message.chat.id, 'Error gathering the horoscope of your sign. Please try again')
    else:
        bot.send_message(message.chat.id, 'Please enter a zodiac sign.')

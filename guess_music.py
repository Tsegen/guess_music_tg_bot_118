import json
import telebot
from urllib.request import Request, urlopen
from random import randint, choice, shuffle
import cowsay
import os
from dotenv import load_dotenv
load_dotenv()

music = [
    {
        "id": "AwACAgIAAxkDAAIBWGQNjm_iM6oCvD3wl1jrOy9tMZcoAAJILgAC-C1pSPQAAXFs5LzWAAEvBA",
        "right": "Anacondaz - Поезда",
        "wrong": [
            "Måneskin - Beggin\'",
            "Queen – Bohemian Rhapsody",
            "Queen – I Want To Break Free"
            ]
        },
    {
        "id": "AwACAgIAAxkDAAIBWmQNjnL0-cLUfOrvgUf06MG8rkBFAAJKLgAC-C1pSBAvBbZJ6cyKLwQ",
        "right": "Måneskin - Beggin\'",
        "wrong": [
            "Queen – Bohemian Rhapsody",
            "Anacondaz - Поезда",
            "Queen – I Want To Break Free"
            ]
        },
    {
        "id": "AwACAgIAAxkDAAIBXGQNjnj3HfFE4o-t8voAARGXNAtx-AACSy4AAvgtaUj-pD3-DpwTOS8E",
        "right": "Queen – Bohemian Rhapsody",
        "wrong": [
            "Måneskin - Beggin\'",
            "Anacondaz - Поезда",
            "Queen – I Want To Break Free"
            ]
        },
    {
        "id": "AwACAgIAAxkDAAIBXmQNjny5llsUuyWDJtdsl27hsebVAAJMLgAC-C1pSENga9uvsPWQLwQ",
        "right": "Queen – I Want To Break Free",
        "wrong": [
            "Måneskin - Beggin\'",
            "Queen – Bohemian Rhapsody",
            "Anacondaz - Поезда"
            ]
        }
]

bot = telebot.TeleBot(os.getenv("TOKEN"))

def generate_markup(right, wrong):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
    answers = wrong + [right]
    shuffle(answers)
    for elem in answers:
        markup.add(elem)
    return markup

users = {}
'''
user_id: 'Правильная_песня'
'''
stats = {}
'''
user_id:
        (1, 3)
'''

@bot.message_handler(commands=['game'])
def game(message):
    global users
    song = choice(music)
    markup = generate_markup(song["right"], song["wrong"])
    bot.send_voice(message.chat.id, song["id"], reply_markup = markup)
    users[message.chat.id] = song["right"]

@bot.message_handler(commands=['stats'])
def game(message):
    right_count, all_count = stats.get(message.chat.id, (0,0) )
    bot.send_message(message.chat.id, f'Правильных ответов: {right_count}, игр: {all_count}')

@bot.message_handler(content_types=['text'])
def check_answer(message):
    right_count, all_count = stats.get(message.chat.id, (0,0) ) ##################
    
    right = users.get(message.chat.id, None)
    if not right:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
        return
    all_count += 1 #############
    if message.text == right:
        text = 'Верно!'
        right_count += 1 ###########
    else:
        text = 'Увы, Вы не угадали. Попробуйте ещё раз!'
    bot.send_message(message.chat.id, text, reply_markup = telebot.types.ReplyKeyboardRemove())
    users.pop(message.chat.id)
    stats[message.chat.id] = (right_count, all_count) ###################

@bot.message_handler(commands=['test'])
def function(message):
        for file in os.listdir('music/'):
            if file.split('.')[-1] == 'ogg':
                music = open('music/' + file, 'rb') # w - write, r - read
                msg = bot.send_voice(message.chat.id, music, None)
                bot.send_message(message.chat.id, msg.voice.file_id )


bot.infinity_polling()

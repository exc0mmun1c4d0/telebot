import telebot
import requests
import translators
from telebot import types


url = "https://burgers1.p.rapidapi.com/burgers"


headers = {
	"X-RapidAPI-Host": "burgers1.p.rapidapi.com",
	"X-RapidAPI-Key": "035726d206mshb212179a4a73aedp1ad7ccjsn4dcd433d6767"
}

response = requests.request("GET", url, headers=headers)
sended_message = []
result = []

number = 0

for i in response.json():
    if number <= 9:
        number += 1
        result.append(str(number) + ') ' + i['name'])
    else:
        break


all_burgers = '\n' + '\n'.join(result)
all_burgers += '\n'

token = '5378869087:AAEjKYn93qPJ-hYFqz8hBcu5m8Pm6sFef0s'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет!! Я бот, который расскажет тебе о самых популярных бургерах на планете. Вот бургеры, про которые я тебе могу рассказать: {all_burgers} Напиши "/button"')


@bot.message_handler(commands=['button'])
def button_message(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    choose1_button = types.KeyboardButton('1')
    choose2_button = types.KeyboardButton('2') 
    choose3_button = types.KeyboardButton('3') 
    choose4_button = types.KeyboardButton('4') 
    choose5_button = types.KeyboardButton('5') 
    choose6_button = types.KeyboardButton('6')
    choose7_button = types.KeyboardButton('7')
    choose8_button = types.KeyboardButton('8')
    choose9_button = types.KeyboardButton('9')
    choose10_button = types.KeyboardButton('10')
    keyboard.add(choose1_button, choose2_button, choose3_button, choose4_button, choose5_button, choose6_button, choose7_button, choose8_button,
                 choose9_button, choose10_button)
        
    bot.send_message(message.chat.id, "Тыкни на кнопку", reply_markup=keyboard)
        

@bot.message_handler(content_types='text')
def message_reply(message):
    if int(message.text) + 1 in range(1, 10):
        # bot.send_message(message.chat.id, f'Вот бургеры, про которые я тебе могу рассказать: {all_burgers}.')

        url = "https://burgers1.p.rapidapi.com/burgers"

        headers = {
	    "X-RapidAPI-Host": "burgers1.p.rapidapi.com",
	    "X-RapidAPI-Key": "035726d206mshb212179a4a73aedp1ad7ccjsn4dcd433d6767"
        }

        queue = {'name': str(result[int(message.text) - 1]).split(') ')[1]}
        response = requests.request("GET", url, headers=headers, params=queue)
        ingredients = str()
        for i in response.json():
	        for j in i['ingredients']:
	            ingredients += translators.google(j, from_language='en', to_language='ru') + ', '

        sended_message.append(response.json()[0]['name'])
        sended_message.append(response.json()[0]['addresses'][0]['country'])
        sended_message.append(translators.google(response.json()[0]['description'], from_language='en', to_language='ru'))

        bot.send_message(message.chat.id, f'Страна - {sended_message[1]}. Описание - {sended_message[2]}.')
        bot.send_message(message.chat.id, f'Ингредиенты - {ingredients[0:len(ingredients) - 2]}.')


bot.infinity_polling()

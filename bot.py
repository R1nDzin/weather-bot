import telebot
import requests

TOKEN = "7606824571:AAHqA-s6DxIAX1QCZ214N3R36b37dNyvoTc"
WEATHER_API = "69fa2cc731deb0ffe06c9456ef9a2074"
bot = telebot.TeleBot(TOKEN)

cities = {
    "Москва": "Moscow",
    "Санкт-Петербург": "Saint Petersburg",
    "Казань": "Kazan"
}

def get_temp(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API}&units=metric&lang=ru"
    response = requests.get(url).json()
    try:
        temp = response.json()["main"]["temp"]
        return temp
    except:
        return None

def get_advice(temp):
    if temp <= 0:
        return "Очень холодно, надевай шапку и куртку! 🥶"
    elif temp <= 10:
        return "Прохладно, нужна куртка 🧥"
    elif temp <= 20:
        return "Комфортная погода, надень кофту или лёгкую куртку 👕"
    else:
        return "Тепло! Отлично подойдёт футболка и шорты ☀️"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*cities.keys())
    bot.send_message(message.chat.id, "Выбери город:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in cities)
def weather(message):
    city_name = message.text
    city_query = cities[city_name]
    temp = get_temp(city=city_name)

    if temp is not None:
        advice = get_advice(temp)
        bot.send_message(message.chat.id, f"🌡 В городе {city_name} сейчас {temp}°C.\n{advice}")
    else:
        bot.send_message(message.chat.id, "Не удалось получить погоду, попробуй позже.")

bot.polling()

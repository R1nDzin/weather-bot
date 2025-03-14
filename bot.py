import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = "7606824571:AAHqA-s6DxIAX1QCZ214N3R36b37dNyvoTc"
bot = telebot.TeleBot(TOKEN)

cities = {
    "Москва": "moscow-4368",
    "Санкт-Петербург": "saint-petersburg-4079",
    "Казань": "kazan-4364"
}

# Функция получения температуры с Gismeteo
def get_temp(city_url):
    url = f"https://www.gismeteo.ru/weather-{city_url}/now/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    temp_span = soup.find('span', class_='unit_temperature_c')
    if temp_span:
        return int(temp_span.text.replace('−', '-').replace('°', '').strip())
    else:
        return None

def get_advice(temp):
    if temp <= 0:
        return "🥶 Очень холодно, надевай шапку и куртку!"
    elif temp <= 10:
        return "Прохладно, нужна куртка 🧥."
    elif temp <= 20:
        return "Комфортно, подойдет легкая куртка или кофта! 👕"
    else:
        return "Тепло, футболка и шорты подойдут отлично ☀️"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(*cities.keys())
    bot.send_message(message.chat.id, "Выбери город:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in cities)
def send_weather(message):
    city = message.text
    city_url = cities[city]
    temp = get_temp(city_url)
    
    if temp is not None:
        advice = get_advice(temp)
        bot.send_message(message.chat.id, f"🌡 Погода в {city} сейчас {temp}°C.\n{advice}")
    else:
        bot.send_message(message.chat.id, "Не удалось получить погоду. Попробуй позже.")

bot.polling()

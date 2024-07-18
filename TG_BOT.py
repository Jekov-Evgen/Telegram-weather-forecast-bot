import requests
import telebot
from token_1 import TOKEN, OWM_API_KEY

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Привет, я скидываю прогноз погоды. Пиши: /weather <город>")

@bot.message_handler(commands=['weather'])
def send_weather(message):
    try:
        city = message.text.split()[1]
        weather = get_weather(city)
        bot.reply_to(message, weather)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите город после команды /weather")

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric&lang=ru'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        return (f"Погода в городе {city}:\n"
                f"Описание: {weather_description}\n"
                f"Температура: {temperature}°C\n"
                f"Ощущается как: {feels_like}°C\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с")
    else:
        return "Город не найден"

bot.polling()
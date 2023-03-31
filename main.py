import telebot

from config import exchanges, TOKEN
from extensions import Converter, ApiException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = f'Привет! \nВведите данные в формате: \nвалюта для конвертации валюта в которую конвертировать количество'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as error:
        bot.reply_to(message, 'Неверное количество параметров!')

    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except ApiException as error:
        bot.reply_to(message, f'Ошибка в команде: \n{error}')


bot.polling()

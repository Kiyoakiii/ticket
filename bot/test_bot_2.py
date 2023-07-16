import telebot
from telebot import types

TOKEN = '6321448809:AAEompqKcjWHFP3bIn8tcV11ZpvjEct2Lr8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Я бот, который может принимать оплату. Нажмите на кнопку ниже, чтобы оплатить.")

    # Создание кнопки оплаты
    prices = [types.LabeledPrice(label='Оплата', amount=10000)] # Сумма в копейках
    provider_token = '381764678:TEST:61736'
    bot.send_invoice(chat_id, title='Оплата', description='Описание оплаты', provider_token=provider_token, currency='RUB', prices=prices, start_parameter='payment', invoice_payload='payload')

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Спасибо за оплату!")

bot.polling()

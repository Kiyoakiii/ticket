from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from datetime import datetime, timedelta
import pars_time
import code 

date_1 = datetime.now().strftime('%d.%m.%Y')
date_2 = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')
date_3 = (datetime.now() + timedelta(days=2)).strftime('%d.%m.%Y')
date_4 = (datetime.now() + timedelta(days=3)).strftime('%d.%m.%Y')
date_5 = (datetime.now() + timedelta(days=4)).strftime('%d.%m.%Y')
date_6 = (datetime.now() + timedelta(days=5)).strftime('%d.%m.%Y')
date_7 = (datetime.now() + timedelta(days=6)).strftime('%d.%m.%Y')
date_8 = (datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')


button1 = InlineKeyboardButton('Москва', callback_data=code.Moscow+"-")
button2 = InlineKeyboardButton('Симферополь', callback_data=code.Simf+"-")
button3 = InlineKeyboardButton('Севастополь', callback_data=code.Sevas+"-")
button4 = InlineKeyboardButton('Мин воды', callback_data=code.MinVod+"-")
button5 = InlineKeyboardButton('Сочи', callback_data=code.Sochi+"-")
button6 = InlineKeyboardButton('Санкт-Петербург', callback_data=code.Spb+"-")

DIRECTION_1 = InlineKeyboardMarkup().row(button1, button2).add(button3, button4, button5, button6)

button_9 = InlineKeyboardButton('Симферополь', callback_data=code.Simf)
button_10 = InlineKeyboardButton('Мин воды', callback_data=code.MinVod)
button_11 = InlineKeyboardButton('Севастополь', callback_data=code.Sevas)
button_12 = InlineKeyboardButton('Москва', callback_data=code.Moscow)

DIRECTION_2 = InlineKeyboardMarkup().row(button_9, button_10).add(button_11, button_12)

button_date_1 = InlineKeyboardButton(f'{date_1}', callback_data=f'{date_1}')
button_date_2 = InlineKeyboardButton(f'{date_2}', callback_data=f'{date_2}')
button_date_3 = InlineKeyboardButton(f'{date_3}', callback_data=f'{date_3}')
button_date_4 = InlineKeyboardButton(f'{date_4}', callback_data=f'{date_4}')
button_date_5 = InlineKeyboardButton(f'{date_5}', callback_data=f'{date_5}')
button_date_6 = InlineKeyboardButton(f'{date_6}', callback_data=f'{date_6}')
button_date_7 = InlineKeyboardButton(f'{date_7}', callback_data=f'{date_7}')
button_date_8 = InlineKeyboardButton(f'{date_8}', callback_data=f'{date_8}')

DATE = InlineKeyboardMarkup().row(button_date_1, button_date_2).add(button_date_3, button_date_4, button_date_5, button_date_6, button_date_7, button_date_8)


button_time_1 = InlineKeyboardButton("1", callback_data="1")
button_time_2 = InlineKeyboardButton("2", callback_data="2")
button_time_3 = InlineKeyboardButton("3", callback_data="3")
button_time_4 = InlineKeyboardButton("4", callback_data="4")

def TIME(count):
     if count == 1:
          return InlineKeyboardMarkup().row(button_time_1)
     elif count == 2:
          return InlineKeyboardMarkup().row(button_time_1, button_time_2)
     elif count == 3:
          return InlineKeyboardMarkup().row(button_time_1, button_time_2).add(button_time_3)
     elif count == 4:
          return InlineKeyboardMarkup().row(button_time_1, button_time_2).add(button_time_3, button_time_4)
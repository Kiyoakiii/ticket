"""
Модуль для определения кнопок.
"""

from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import code_city

date_1 = datetime.now().strftime("%d.%m.%Y")
date_2 = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
date_3 = (datetime.now() + timedelta(days=2)).strftime("%d.%m.%Y")
date_4 = (datetime.now() + timedelta(days=3)).strftime("%d.%m.%Y")
date_5 = (datetime.now() + timedelta(days=4)).strftime("%d.%m.%Y")
date_6 = (datetime.now() + timedelta(days=5)).strftime("%d.%m.%Y")
date_7 = (datetime.now() + timedelta(days=6)).strftime("%d.%m.%Y")
date_8 = (datetime.now() + timedelta(days=7)).strftime("%d.%m.%Y")


button1 = InlineKeyboardButton(
    text="Москва",
    callback_data=code_city.MOSCOW + "-")
button2 = InlineKeyboardButton(
    text="Симферополь",
    callback_data=code_city.SIMF + "-")
button3 = InlineKeyboardButton(
    text="Севастополь",
    callback_data=code_city.SEVAS + "-")
button4 = InlineKeyboardButton(text="Мин воды",
                               callback_data=code_city.MINVOD + "-")
button5 = InlineKeyboardButton(
    text="Сочи",
    callback_data=code_city.SOCHI + "-")
button6 = InlineKeyboardButton(
    text="Санкт-Петербург",
    callback_data=code_city.SPB + "-")
button7 = InlineKeyboardButton(
    text="Казань",
    callback_data=code_city.KAZAN + "-")
button8 = InlineKeyboardButton(
    text="Евпатория",
    callback_data=code_city.EVP + "-")

DIRECTION_1 = InlineKeyboardMarkup(inline_keyboard=[
    [button1, button2],
    [button3, button4],
    [button5, button6],
    [button7, button8]
])

button_9 = InlineKeyboardButton(
    text="Симферополь",
    callback_data=code_city.SIMF)
button_10 = InlineKeyboardButton(
    text="Мин воды",
    callback_data=code_city.MINVOD)
button_11 = InlineKeyboardButton(
    text="Севастополь",
    callback_data=code_city.SEVAS)
button_12 = InlineKeyboardButton(text="Москва", callback_data=code_city.MOSCOW)
button_13 = InlineKeyboardButton(text="Казань", callback_data=code_city.KAZAN)
button_14 = InlineKeyboardButton(text="Сочи", callback_data=code_city.SOCHI)

DIRECTION_2 = InlineKeyboardMarkup(inline_keyboard=[
    [button_9, button_10],
    [button_11, button_12],
    [button_13, button_14]
])

button_date_1 = InlineKeyboardButton(
    text=f"{date_1}", callback_data=f"{date_1}")
button_date_2 = InlineKeyboardButton(
    text=f"{date_2}", callback_data=f"{date_2}")
button_date_3 = InlineKeyboardButton(
    text=f"{date_3}", callback_data=f"{date_3}")
button_date_4 = InlineKeyboardButton(
    text=f"{date_4}", callback_data=f"{date_4}")
button_date_5 = InlineKeyboardButton(
    text=f"{date_5}", callback_data=f"{date_5}")
button_date_6 = InlineKeyboardButton(
    text=f"{date_6}", callback_data=f"{date_6}")
button_date_7 = InlineKeyboardButton(
    text=f"{date_7}", callback_data=f"{date_7}")
button_date_8 = InlineKeyboardButton(
    text=f"{date_8}", callback_data=f"{date_8}")
button_date_9 = InlineKeyboardButton(text="Другая", callback_data="any")

DATE = InlineKeyboardMarkup(inline_keyboard=[
    [button_date_1, button_date_2],
    [button_date_3, button_date_4],
    [button_date_5, button_date_6],
    [button_date_7, button_date_8],
    [button_date_9]
])


ANY_DATE = types.ReplyKeyboardRemove()

button_time_1 = InlineKeyboardButton(text="1", callback_data="1")
button_time_2 = InlineKeyboardButton(text="2", callback_data="2")
button_time_3 = InlineKeyboardButton(text="3", callback_data="3")
button_time_4 = InlineKeyboardButton(text="4", callback_data="4")

button_seat_1 = InlineKeyboardButton(text="Низ", callback_data="низ")
button_seat_2 = InlineKeyboardButton(text="Верх", callback_data="верх")
button_seat_3 = InlineKeyboardButton(text="Любая", callback_data="любая")


SEAT = InlineKeyboardMarkup(inline_keyboard=[
    [button_seat_1, button_seat_2],
    [button_seat_3]
])


def generate_time_keyboard(count: int) -> InlineKeyboardMarkup:
    """
    Генерирует InlineKeyboardMarkup в зависимости от количества временных кнопок.

    Args:
        count (int): Количество временных кнопок.

    Returns:
        InlineKeyboardMarkup: Inline клавиатура с кнопками времени.
    """
    if count == 1:
        return (InlineKeyboardMarkup(inline_keyboard=[
            [button_time_1]
        ])
        )
    if count == 2:
        return (InlineKeyboardMarkup(inline_keyboard=[
            [button_time_1, button_time_2]
        ]))
    if count == 3:
        return (
            InlineKeyboardMarkup(inline_keyboard=[
                [button_time_1, button_time_2],
                [button_time_3]
            ])
        )
    if count == 4:
        return (
            InlineKeyboardMarkup(inline_keyboard=[
                [button_time_1, button_time_2],
                [button_time_3, button_time_4]
            ])
        )
    return InlineKeyboardMarkup(inline_keyboard=[])

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
import inline_keyboard
import messages
import config
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import pika 
from datetime import datetime, timedelta
import code
import pars_time
import pars_ticket
from aiogram import types
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import asyncio


date_1 = datetime.now().strftime('%d.%m.%Y')
date_2 = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')
date_3 = (datetime.now() + timedelta(days=2)).strftime('%d.%m.%Y')
date_4 = (datetime.now() + timedelta(days=3)).strftime('%d.%m.%Y')
date_5 = (datetime.now() + timedelta(days=4)).strftime('%d.%m.%Y')
date_6 = (datetime.now() + timedelta(days=5)).strftime('%d.%m.%Y')
date_7 = (datetime.now() + timedelta(days=6)).strftime('%d.%m.%Y')
date_8 = (datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')


class Gen(StatesGroup):
    wait_for_input_api_key = State()
    wait_for_input_api_secret = State()
    wait_for_input_num_of_trades = State()
    wait_for_answer = State()

logging.basicConfig(level=logging.INFO)
storage=MemoryStorage()
bot = Bot(token=config.BOT_API_TOKEN)
sum = 0
dp = Dispatcher(bot, storage=storage)


api_key=''
api_secret=''

@dp.message_handler(commands=['start'])
async def show_info(message: types.Message):
    await message.reply(text=messages.reg(), reply_markup=inline_keyboard.DIRECTION_1)



#   запрос на Москва
@dp.callback_query_handler(text=code.Moscow+"-")
async def show_info(callback_query: types.CallbackQuery):
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.to(), reply_markup=inline_keyboard.DIRECTION_2)
    departure_place = code.Moscow

#   запрос на Симферополь
@dp.callback_query_handler(text=code.Simf+"-")
async def show_info(callback_query: types.CallbackQuery):
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.to(), reply_markup=inline_keyboard.DIRECTION_2)
    departure_place = code.Simf

#   запрос на Севастополь
@dp.callback_query_handler(text=code.Sevas+"-")
async def show_info(callback_query: types.CallbackQuery):
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.to(), reply_markup=inline_keyboard.DIRECTION_2)
    departure_place = code.Sevas

#   запрос на Минводы
@dp.callback_query_handler(text=code.MinVod+"-")
async def show_info(callback_query: types.CallbackQuery):
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.to(), reply_markup=inline_keyboard.DIRECTION_2)
    departure_place = code.MinVod

#   запрос на Сочи
@dp.callback_query_handler(text=code.Sochi+"-")
async def show_info(callback_query: types.CallbackQuery):
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.to(), reply_markup=inline_keyboard.DIRECTION_2)
    departure_place = code.Sochi

#   запрос на Спб
@dp.callback_query_handler(text=code.Spb+"-")
async def show_info(callback_query: types.CallbackQuery):
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.to(), reply_markup=inline_keyboard.DIRECTION_2)
    departure_place = code.Spb


#   Отправление
#   Переход с прибытия на дату
#   запрос на МинВоды
@dp.callback_query_handler(text=code.MinVod)
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.date(), reply_markup=inline_keyboard.DATE)
    place_of_arrival = code.MinVod

#   запрос на Симферополь
@dp.callback_query_handler(text=code.Simf)
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.date(), reply_markup=inline_keyboard.DATE)
    place_of_arrival = code.Simf

#   запрос на Севастополь
@dp.callback_query_handler(text=code.Sevas)
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.date(), reply_markup=inline_keyboard.DATE)
    place_of_arrival = code.Sevas

#   запрос на Москва
@dp.callback_query_handler(text=code.Moscow)
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.date(), reply_markup=inline_keyboard.DATE)
    place_of_arrival = code.Moscow


#   Запрос на дату
#   Переход с даты на время
@dp.callback_query_handler(text=f'{date_1}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_1, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_1), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_1
@dp.callback_query_handler(text=f'{date_2}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_2, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    print(count)
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_2), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_2

@dp.callback_query_handler(text=f'{date_3}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_3, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_3), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_3

@dp.callback_query_handler(text=f'{date_4}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_4, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_4), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_4

@dp.callback_query_handler(text=f'{date_5}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_5, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_5), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_5

@dp.callback_query_handler(text=f'{date_6}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_6, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_6), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_6

@dp.callback_query_handler(text=f'{date_7}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_7, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_7), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_7

@dp.callback_query_handler(text=f'{date_8}')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(date_8, departure_place, place_of_arrival) 
    count = time_travel.count(")")
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(date_8), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))
    arrival_date = date_8





@dp.callback_query_handler(text='1')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel, cancel_flag
    date = arrival_date
    cancel_flag = False
    time_ar = time_travel.split('1) Отправление:  ')[1].split(' ')[0]
    await bot.send_message(callback_query.from_user.id, text=messages.time_departure(place_of_arrival, departure_place, arrival_date, time_ar))
    
    webdriver_path = "A:\Учёба\практика 2 курс\chromedriver.exe"
    print(date)

    # Создаем экземпляр Chrome WebDriver
    print("!!!!!")
    options = webdriver.ChromeOptions()
    # Запуск в безголовом режиме (без открытия окна браузера)
    #options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Загружаем страницу с помощью Selenium WebDriver
    url = f"https://grandtrain.ru/tickets/{departure_place}-{place_of_arrival}/{date}/"
    driver.get(url)
    text = ''
    ans = 'Свободных мест нет'
    cancel_flag == False
    try:
        text = driver.find_element(
            By.XPATH, '/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[1]/div[2]/div[4]/div[1]').text
        print(text)
        ans += text    
    except Exception:
        pass
    time_num = 1
    time.sleep(3)
    await asyncio.sleep(1)
    while (ans == 'Свободных мест нет' or ans == '' or 'Люкс' in ans) and cancel_flag == False:
        driver.refresh()
        await asyncio.sleep(10)
        ans = ''
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[1]').text
            print(text)
            ans += text
            print('4:',text)
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[2]').text
            print(text)     
            if text != "Выбрать места":
                ans += text
                print('5:',text)
            else:
                ans = 'Свободных мест нет'
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[3]').text
            print('6:',text)
            ans += text
        except Exception:
            pass

        print('ans = ', ans)

    if cancel_flag == False:
        await bot.send_message(callback_query.from_user.id, text=messages.ticket_is_ready(url, ans))
    else:
        await bot.send_message(callback_query.from_user.id, text=messages.cancel())


@dp.message_handler(commands=['cancel'])
async def cancel_cmd_handler(message: types.Message):
    global cancel_flag
    print('Cancel command received')
    cancel_flag = True
    await message.answer(text="Я получил команду на отмену операции.")

    
@dp.callback_query_handler(text='2')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel, cancel_flag
    date = arrival_date
    cancel_flag = False
    time_ar = time_travel.split('2) Отправление:  ')[1].split(' ')[0]
    await bot.send_message(callback_query.from_user.id, text=messages.time_departure(place_of_arrival, departure_place, arrival_date, time_ar))
    
    webdriver_path = "A:\Учёба\практика 2 курс\chromedriver.exe"
    print(date)

    # Создаем экземпляр Chrome WebDriver
    print("!!!!!")
    options = webdriver.ChromeOptions()
    # Запуск в безголовом режиме (без открытия окна браузера)
    #options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Загружаем страницу с помощью Selenium WebDriver
    url = f"https://grandtrain.ru/tickets/{departure_place}-{place_of_arrival}/{date}/"
    driver.get(url)
    text = ''
    ans = 'Свободных мест нет'
    cancel_flag == False
    try:
        text = driver.find_element(
            By.XPATH, '/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[1]/div[2]/div[4]/div[1]').text
        print(text)
        ans += text    
    except Exception:
        pass
    time_num = 2
    time.sleep(3)
    await asyncio.sleep(1)
    while (ans == 'Свободных мест нет' or ans == '' or 'Люкс' in ans) and cancel_flag == False:
        driver.refresh()
        await asyncio.sleep(10)
        ans = ''
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[1]').text
            print(text)
            ans += text
            print('4:',text)
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[2]').text
            print(text)     
            if text != "Выбрать места":
                ans += text
                print('5:',text)
            else:
                ans = 'Свободных мест нет'
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[3]').text
            print('6:',text)
            ans += text
        except Exception:
            pass

        print('ans = ', ans)

    if cancel_flag == False:
        await bot.send_message(callback_query.from_user.id, text=messages.ticket_is_ready(url, ans))
    else:
        await bot.send_message(callback_query.from_user.id, text=messages.cancel())

@dp.callback_query_handler(text='3')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel, cancel_flag
    date = arrival_date
    cancel_flag = False
    time_ar = time_travel.split('3) Отправление:  ')[1].split(' ')[0]
    await bot.send_message(callback_query.from_user.id, text=messages.time_departure(place_of_arrival, departure_place, arrival_date, time_ar))
    
    webdriver_path = "A:\Учёба\практика 2 курс\chromedriver.exe"
    print(date)

    # Создаем экземпляр Chrome WebDriver
    print("!!!!!")
    options = webdriver.ChromeOptions()
    # Запуск в безголовом режиме (без открытия окна браузера)
    #options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Загружаем страницу с помощью Selenium WebDriver
    url = f"https://grandtrain.ru/tickets/{departure_place}-{place_of_arrival}/{date}/"
    driver.get(url)
    text = ''
    ans = 'Свободных мест нет'
    cancel_flag == False
    try:
        text = driver.find_element(
            By.XPATH, '/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[1]/div[2]/div[4]/div[1]').text
        print(text)
        ans += text    
    except Exception:
        pass
    time_num = 3
    time.sleep(3)
    await asyncio.sleep(1)
    while (ans == 'Свободных мест нет' or ans == '' or 'Люкс' in ans) and cancel_flag == False:
        driver.refresh()
        await asyncio.sleep(10)
        ans = ''
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[1]').text
            print(text)
            ans += text
            print('4:',text)
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[2]').text
            print(text)     
            if text != "Выбрать места":
                ans += text
                print('5:',text)
            else:
                ans = 'Свободных мест нет'
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[3]').text
            print('6:',text)
            ans += text
        except Exception:
            pass

        print('ans = ', ans)

    if cancel_flag == False:
        await bot.send_message(callback_query.from_user.id, text=messages.ticket_is_ready(url, ans))
    else:
        await bot.send_message(callback_query.from_user.id, text=messages.cancel())

@dp.callback_query_handler(text='4')
async def show_info(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel, cancel_flag
    date = arrival_date
    cancel_flag = False
    time_ar = time_travel.split('4) Отправление:  ')[1].split(' ')[0]
    await bot.send_message(callback_query.from_user.id, text=messages.time_departure(place_of_arrival, departure_place, arrival_date, time_ar))
    
    webdriver_path = "A:\Учёба\практика 2 курс\chromedriver.exe"
    print(date)

    # Создаем экземпляр Chrome WebDriver
    print("!!!!!")
    options = webdriver.ChromeOptions()
    # Запуск в безголовом режиме (без открытия окна браузера)
    #options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Загружаем страницу с помощью Selenium WebDriver
    url = f"https://grandtrain.ru/tickets/{departure_place}-{place_of_arrival}/{date}/"
    driver.get(url)
    text = ''
    ans = 'Свободных мест нет'
    cancel_flag == False
    try:
        text = driver.find_element(
            By.XPATH, '/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[1]/div[2]/div[4]/div[1]').text
        print(text)
        ans += text    
    except Exception:
        pass
    time_num = 4
    time.sleep(3)
    await asyncio.sleep(1)
    while (ans == 'Свободных мест нет' or ans == '' or 'Люкс' in ans) and cancel_flag == False:
        driver.refresh()
        await asyncio.sleep(10)
        ans = ''
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[1]').text
            print(text)
            ans += text
            print('4:',text)
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[2]').text
            print(text)     
            if text != "Выбрать места":
                ans += text
                print('5:',text)
            else:
                ans = 'Свободных мест нет'
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[3]').text
            print('6:',text)
            ans += text
        except Exception:
            pass

        print('ans = ', ans)

    if cancel_flag == False:
        await bot.send_message(callback_query.from_user.id, text=messages.ticket_is_ready(url, ans))
    else:
        await bot.send_message(callback_query.from_user.id, text=messages.cancel())



if __name__ == '__main__':
    global departure_place
    executor.start_polling(dp, skip_updates=True)

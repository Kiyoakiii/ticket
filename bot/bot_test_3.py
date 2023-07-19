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
from aiogram.dispatcher import FSMContext
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
    wait_for_input_date = State()
    wait_for_answer = State()

logging.basicConfig(level=logging.INFO)
storage=MemoryStorage()
bot = Bot(token=config.API_TOKEN)
sum = 0
dp = Dispatcher(bot, storage=storage)


api_key=''
api_secret=''

#   Запуск бота. Выбор отправления
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.reply(text=messages.reg(), reply_markup=inline_keyboard.DIRECTION_1)

#   Остановка бота
@dp.message_handler(commands=['cancel'])
async def cancel_bot(message: types.Message):
    global cancel_flag
    print('Cancel command received')
    cancel_flag = True
    await message.answer(text="Я получил команду на отмену операции.")

#   Выбор прибытия 
@dp.callback_query_handler(lambda callback_query: callback_query.data in [code.Moscow+"-", code.Simf+"-", code.Sevas+"-", code.MinVod+"-",code.Sochi+"-",code.Spb+"-"])
async def train_departure(callback_query: types.CallbackQuery):
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.to(), reply_markup=inline_keyboard.DIRECTION_2)
    departure_place = callback_query.data

#   Выбор даты
@dp.callback_query_handler(lambda callback_query: callback_query.data in [code.Moscow, code.Sevas, code.Simf, code.MinVod])
async def date_picker(callback_query: types.CallbackQuery):
    global place_of_arrival
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.date(), reply_markup=inline_keyboard.DATE)
    place_of_arrival = callback_query.data

#   Пользователь вводит свою дату
@dp.callback_query_handler(text='any')
async def user_date(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Введите дату', reply_markup=types.ReplyKeyboardRemove())
    await Gen.wait_for_input_date.set() 

@dp.message_handler(state=Gen.wait_for_input_date)
async def show_info_any_date(message: types.Message, state: FSMContext):
    await state.finish()
    global place_of_arrival, departure_place, arrival_date, time_travel, date_any
    date_any = message.text
    print(date_any)
    time_travel = await pars_time.get_time(date_any, departure_place, place_of_arrival)
    if time_travel ==  'err':
        await bot.send_message(message.from_user.id, text=messages.time_none(date_any), reply_markup=inline_keyboard.DATE)
    else:
        await bot.send_message(message.from_user.id, text=messages.seat(), reply_markup=inline_keyboard.SEAT)
    arrival_date = date_any

#   Выбор полки
@dp.callback_query_handler(lambda callback_query: callback_query.data in [f'{date_1}', f'{date_2}', f'{date_3}',f'{date_4}', f'{date_5}', f'{date_6}',f'{date_7}', f'{date_8}'])
async def wagon_shelf_selection(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(callback_query.data, departure_place, place_of_arrival) 
    if time_travel ==  'err':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.time_none(callback_query.data), reply_markup=inline_keyboard.DATE)
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, text=messages.seat(), reply_markup=inline_keyboard.SEAT)
    arrival_date = callback_query.data

#   Выбор времени 
@dp.callback_query_handler(lambda callback_query: callback_query.data in ['низ', 'верх', 'любая'])
async def time_selection(callback_query: types.CallbackQuery):
    global seat
    count = time_travel.count(")")
    seat = callback_query.data
    await bot.send_message(callback_query.from_user.id, text=messages.time(time_travel), reply_markup=inline_keyboard.TIME(count))

#   Мониторинг
@dp.callback_query_handler(lambda callback_query: callback_query.data in ['1', '2', '3', '4'])
async def pars_wagon(callback_query: types.CallbackQuery):
    global place_of_arrival, departure_place, arrival_date, time_travel, cancel_flag, seat
    date = arrival_date
    cancel_flag = False
    time_ar = time_travel.split(f'{callback_query.data}) Отправление:  ')[1].split(' ')[0]
    await bot.send_message(callback_query.from_user.id, text=messages.time_departure(place_of_arrival, departure_place, arrival_date, time_ar, seat))  
    webdriver_path = "A:\Учёба\практика 2 курс\chromedriver.exe"
    print(date)

    # Создаем экземпляр Chrome WebDriver
    print("!!!!!")
    options = webdriver.ChromeOptions()
    # Запуск в безголовом режиме (без открытия окна браузера)
    options.add_argument('--headless')
    options.add_argument('--log-level=1')
    options.add_argument('--log-level=2')
    options.add_argument('--log-level=3')
    options.page_load_strategy = 'normal'
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://grandtrain.ru/tickets/{departure_place}{place_of_arrival}/{date}/"
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

    try:
        new_seat = driver.find_element(
            By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/div[3]').text
        #print(new_seat)
        ans += text    
    except Exception:
        pass 

    try:
        new_seat = driver.find_element(
            By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[3]/div[1]/div[3]').text
        #print(new_seat)
    except Exception:
        pass

    # /html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/div[3]
    # /html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[3]/div[1]/div[3]
    time_num = callback_query.data
    new_seat = ''
    start_time = time.time()
    time.sleep(3)
    await asyncio.sleep(1)
    print("seat = ", seat)
    old_time =time.time() 
    message = await bot.send_message(callback_query.from_user.id, text=f"Далее каждые 10 минут я буду сообщать Вам, сколько вы сэкономили времени")
    while ((ans == 'Свободных мест нет') or (ans == '')) and (cancel_flag == False):
        driver.refresh()
        now_time = time.time()
        time_free = round((now_time - start_time)/60)
        
        print('time_free = ', time_free )
        print('round((now_time-old_time )/ 60) = ', round((now_time-old_time )/ 60))
        if  start_time > 0 and (round((now_time-old_time )/ 60))==10:
            old_time = time.time()
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message.message_id, text=f"Вы сэкономили: {time_free} минут.")
        ans = ''
        
        await asyncio.sleep(10)
        try:
            new_seat = driver.find_element(
                By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/div[3]').text
            #print(new_seat)
            ans += ' ' + text    
        except Exception:
            pass 

        try:
            new_seat = driver.find_element(
                By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[3]/div[1]/div[3]').text
            #print(new_seat)
        except Exception:
            pass

        try:
            new_seat = driver.find_element(
                By.XPATH, '/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[4]/div[1]/div[3]').text
            #print(new_seat)
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[1]').text
            print(text)
            ans += ' ' + text
            print('4:',text)
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[2]').text
            print(text)     
            if text != "Выбрать места":
                ans += ' ' + text
                print('5:',text)
            else:
                ans = 'Свободных мест нет'
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[3]').text
            print('6:',text)
            ans += ' ' + text
        except Exception:
            pass

        print('1ans = ', ans)

        if seat != 'любая' and seat not in new_seat:
            ans = ''

        print('2ans = ', ans)
        if not("Купе" in ans) and not("Плац" in ans):
            ans = ''

        print('3ans = ', ans)

    print('ans = ', ans)
    if cancel_flag == False:
        await bot.send_message(callback_query.from_user.id, text=messages.ticket_is_ready(url, ans))
    else:
        await bot.send_message(callback_query.from_user.id, text=messages.cancel())


if __name__ == '__main__':
    global departure_place
    executor.start_polling(dp, skip_updates=True)

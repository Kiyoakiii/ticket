"""
Основной модуль.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import code_city
import config
import inline_keyboard
import messages
import pars_time

date_1 = datetime.now().strftime("%d.%m.%Y")
date_2 = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
date_3 = (datetime.now() + timedelta(days=2)).strftime("%d.%m.%Y")
date_4 = (datetime.now() + timedelta(days=3)).strftime("%d.%m.%Y")
date_5 = (datetime.now() + timedelta(days=4)).strftime("%d.%m.%Y")
date_6 = (datetime.now() + timedelta(days=5)).strftime("%d.%m.%Y")
date_7 = (datetime.now() + timedelta(days=6)).strftime("%d.%m.%Y")
date_8 = (datetime.now() + timedelta(days=7)).strftime("%d.%m.%Y")


class Gen(StatesGroup):
    """
    Состояния генератора состояний для управления ботом.

    Attributes:
        wait_for_input_date: Состояние ожидания ввода даты.
        wait_for_answer: Состояние ожидания ответа.
    """

    wait_for_input_date = State()
    wait_for_answer = State()


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot, storage=storage)
CANCEL_FLAG = False


date_any, place_of_arrival, departure_place, arrival_date, time_travel = '', '', '', '', ''
seat = 'Любая'
place_of_arrival, departure_place = '', ''


@dp.message_handler(commands=["start"])
async def start_bot(message: types.Message) -> None:
    """
    Обрабатывает команду /start для запуска бота и начала процесса выбора места отправления.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await message.reply(text=messages.reg(), reply_markup=inline_keyboard.DIRECTION_1)


@dp.message_handler(commands=["cancel"])
async def cancel_bot(message: types.Message) -> None:
    """
    Обрабатывает команду /cancel для отмены операции.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    global CANCEL_FLAG
    print("Cancel command received")
    CANCEL_FLAG = True
    await message.answer(text="Я получил команду на отмену операции.")


#   Выбор прибытия


@dp.callback_query_handler(
    lambda callback_query: callback_query.data
    in [
        code_city.MOSCOW + "-",
        code_city.SIMF + "-",
        code_city.SEVAS + "-",
        code_city.MINVOD + "-",
        code_city.SOCHI + "-",
        code_city.SPB + "-",
        code_city.KAZAN + "-",
        code_city.EVP + "-",
    ]
)
async def train_departure(callback_query: types.CallbackQuery) -> None:
    """
    Обрабатывает callback-запросы для выбора пункта отправления поезда.

    Args:
        callback_query (types.CallbackQuery): Объект callback-запроса.

    Returns:
        None
    """
    global departure_place
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.to(),
        reply_markup=inline_keyboard.DIRECTION_2,
    )
    departure_place = callback_query.data


#   Выбор даты


@dp.callback_query_handler(
    lambda callback_query: callback_query.data
    in [
        code_city.MOSCOW,
        code_city.SEVAS,
        code_city.SIMF,
        code_city.MINVOD,
        code_city.KAZAN,
        code_city.EVP,
        code_city.SOCHI,
    ]
)
async def date_picker(callback_query: types.CallbackQuery) -> None:
    """
    Отправляет сообщение с клавиатурой выбора даты пользователю.

    Args:
        callback_query (types.CallbackQuery): Объект callback-запроса.

    Returns:
        None
    """
    global place_of_arrival
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.date(),
        reply_markup=inline_keyboard.DATE,
    )
    place_of_arrival = callback_query.data


@dp.callback_query_handler(text="any")
async def user_date(message: types.Message):
    """
    Обрабатывает callback-запросы для получения даты от пользователя.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await bot.send_message(
        message.from_user.id,
        text="Введите дату",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await Gen.wait_for_input_date.set()


@dp.message_handler(state=Gen.wait_for_input_date)
async def show_info_any_date(
        message: types.Message,
        state: FSMContext) -> None:
    """
    Обрабатывает сообщения пользователя в состоянии ожидания ввода даты.

    Args:
        message: Объект сообщения от пользователя.
        state: Контекст состояния.
    """
    await state.finish()
    global place_of_arrival, departure_place, arrival_date, time_travel, date_any
    date_any = message.text
    print(date_any)
    time_travel = await pars_time.get_time(date_any, departure_place, place_of_arrival)
    if time_travel == "err":
        await bot.send_message(
            message.from_user.id,
            text=messages.time_none(date_any),
            reply_markup=inline_keyboard.DATE,
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text=messages.seat(),
            reply_markup=inline_keyboard.SEAT,
        )
    arrival_date = date_any  # Определение переменной arrival_date


#   Выбор полки


@dp.callback_query_handler(
    lambda callback_query: callback_query.data
    in [
        f"{date_1}",
        f"{date_2}",
        f"{date_3}",
        f"{date_4}",
        f"{date_5}",
        f"{date_6}",
        f"{date_7}",
        f"{date_8}",
    ]
)
async def wagon_shelf_selection(callback_query: types.CallbackQuery) -> None:
    """
    Обрабатывает выбор места отправления.

    Args:
        callback_query (types.CallbackQuery): Объект callback-запроса.

    Returns:
        None
    """
    global place_of_arrival, departure_place, arrival_date, time_travel
    time_travel = await pars_time.get_time(
        callback_query.data, departure_place, place_of_arrival
    )
    if time_travel == "err":
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id,
            text=messages.time_none(callback_query.data),
            reply_markup=inline_keyboard.DATE,
        )
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id,
            text=messages.seat(),
            reply_markup=inline_keyboard.SEAT,
        )
    arrival_date = callback_query.data


#   Выбор времени


@dp.callback_query_handler(
    lambda callback_query: callback_query.data in ["низ", "верх", "любая"]
)
async def time_selection(callback_query: types.CallbackQuery) -> None:
    """
    Обрабатывает выбор времени отправления.

    Args:
        callback_query (types.CallbackQuery): Объект callback-запроса.

    Returns:
        None
    """
    global seat
    count = time_travel.count(")")
    seat = callback_query.data
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.time(time_travel),
        reply_markup=inline_keyboard.generate_time_keyboard(count),
    )


#   Мониторинг


@dp.callback_query_handler(
    lambda callback_query: callback_query.data in ["1", "2", "3", "4"]
)
async def pars_wagon(callback_query: types.CallbackQuery) -> None:
    """
    Обрабатывает поиск билета.

    Args:
        callback_query (types.CallbackQuery): Объект callback-запроса.

    Returns:
        None
    """
    global place_of_arrival, departure_place, arrival_date, time_travel, CANCEL_FLAG, seat
    date = arrival_date
    CANCEL_FLAG = False
    time_ar = time_travel.split(f"{callback_query.data}) Отправление:  ")[
        1].split(" ")[0]
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.time_departure(
            place_of_arrival, departure_place, arrival_date, time_ar, seat
        ),
    )
    webdriver_path = "A:\\Учёба\\практика 2 курс\\chromedriver.exe"
    options = webdriver.ChromeOptions()

    # Запуск в безголовом режиме (без открытия окна браузера)
    options.add_argument("--headless")
    options.add_argument("--log-level=1")
    options.add_argument("--log-level=2")
    options.add_argument("--log-level=3")
    options.page_load_strategy = "normal"

    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://grandtrain.ru/tickets/{departure_place}{place_of_arrival}/{date}/"
    driver.get(url)
    text = ""
    ans = "Свободных мест нет"
    CANCEL_FLAG = False
    try:
        text = driver.find_element(
            By.XPATH,
            "/html/body/main/div[3]/form/div/\
                div[4]/div/div[1]/div[1]/div[2]/div[4]/div[1]",
        ).text
        print(text)
        ans += text
    except NoSuchElementException:
        print("Element not found")

    try:
        new_seat = driver.find_element(
            By.XPATH,
            "/html/body/main/div[3]/form/div/\
                div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/div[3]",
        ).text
        # print(new_seat)
        # print('case 1')
        ans += text
    except NoSuchElementException:
        print("Element not found")

    try:
        new_seat = driver.find_element(
            By.XPATH,
            "/html/body/main/div[3]/form/div/\
                div[2]/div/div[1]/div[2]/div[2]/div[4]/div[3]/div[1]/div[3]",
        ).text
        # print(new_seat)
        # print('case 2')
    except NoSuchElementException:
        print("Element not found")

    # очень давно
    # /html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/div[3]
    # /html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[3]/div[1]/div[3]
    time_num = callback_query.data
    new_seat = ""
    start_time = time.time()
    time.sleep(3)
    await asyncio.sleep(1)
    # print("seat = ", seat)
    old_time = time.time()
    message = await bot.send_message(
        callback_query.from_user.id,
        text="Далее каждые 10 минут я буду сообщать Вам, сколько вы сэкономили времени",
    )
    while (
        ans in (
            'Свободных мест нет',
            '') or ans == "") and (
            CANCEL_FLAG is False):
        driver.refresh()
        now_time = time.time()
        time_free = round((now_time - start_time) / 60)

        # print('time_free = ', time_free )
        if start_time > 0 and (round((now_time - old_time) / 60)) == 10:
            old_time = time.time()
            await bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                message_id=message.message_id,
                text=f"Вы сэкономили: {time_free} минут.",
            )
        ans = ""

        await asyncio.sleep(10)
        try:
            new_seat = driver.find_element(
                By.XPATH,
                "/html/body/main/div[3]/form/div/div[2]/\
                    div/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/div[3]",
            ).text
            # print('new_seat = ', new_seat)
            ans += " " + new_seat
            # print('case 3')
        except NoSuchElementException:
            print("Element not found")

        try:
            new_seat = driver.find_element(
                By.XPATH,
                "/html/body/main/div[3]/form/div/div[2]/\
                    div/div[1]/div[2]/div[2]/div[4]/div[3]/div[1]/div[3]",
            ).text
            # print('1new_seat = ', new_seat)
            # print('case 4')
        except NoSuchElementException:
            print("Element not found")

        try:
            new_seat = driver.find_element(
                By.XPATH,
                "/html/body/main/div[3]/form/div/div[2]/\
                    div/div[1]/div[2]/div[2]/div[4]/div[4]/div[1]/div[3]",
            ).text
            # print('2new_seat = ', new_seat)
            ans += " " + new_seat
            # print('case 5')
        except NoSuchElementException:
            print("Element not found")
        # смотреть сочи
        try:
            new_seat = driver.find_element(
                By.XPATH,
                "/html/body/main/div[3]/form/div/div[4]/\
                    div/div[1]/div/div[2]/div[4]/div[2]/div[1]",
            ).text
            print("ans = ", new_seat)
            ans += " " + new_seat
            print("case 5")
        except NoSuchElementException:
            print("Element not found")
        try:
            new_seat = driver.find_element(
                By.XPATH,
                "/html/body/main/div[3]/form/div/div[4]/\
                    div/div[1]/div/div[2]/div[4]/div[3]/div[1]",
            ).text
            ans += " " + new_seat
            print("ans = ", ans)
            print("case 6")
        except NoSuchElementException:
            print("Element not found")
        try:
            new_seat = driver.find_element(
                By.XPATH,
                "/html/body/main/div[3]/form/div/div[4]/\
                    div/div[1]/div/div[2]/div[4]/div[4]/div[1]",
            ).text
            ans += " " + new_seat
            print("ans = ", ans)
            print("case 7")
        except NoSuchElementException:
            print("Element not found")

        try:
            text = driver.find_element(
                By.XPATH,
                f"/html/body/main/div[3]/form/div/div[4]/\
                    div/div[1]/div[{time_num}]/div[2]/div[4]/div[1]",
            ).text
            if 'Осталось' not in text:
                ans += " " + text
                print("ans = ", ans)
                print("case 7")

            # print('4:',text)
        except NoSuchElementException:
            print("Element not found")

        try:
            text = driver.find_element(
                By.XPATH,
                f"/html/body/main/div[3]/form/div/div[2]/\
                    div/div[1]/div[{time_num}]/div[2]/div[4]/div[2]",
            ).text
            # print(text)
            # if text != "Выбрать места":
            #    ans += " " + text
            #    # print('5:',text)
            # else:
            #    ans = "Свободных мест нет"
            if 'Осталось' not in text:
                ans += " " + text
                print("ans = ", ans)
                print("case 8")
        except NoSuchElementException:
            print("Element not found")
        try:
            text = driver.find_element(
                By.XPATH,
                f"/html/body/main/div[3]/form/div/div[2]/\
                    div/div[1]/div[{time_num}]/div[2]/div[4]/div[3]",
            ).text
            # print('6:',text)
            if 'Осталось' not in text:
                ans += " " + text
                print("ans = ", ans)
                print("case 9")
        except NoSuchElementException:
            print("Element not found")

        try:
            lux_position = ans.find("Люкс")
            # Обрезаем строку до позиции "Люкс"
            ans = ans[:lux_position]
        except ValueError:
            pass

        print("Проверяем какие билеты есть:", ans)
        # print(seat, new_seat)

        # Эта часть кода для казань-симф. Проверка купе низ.
        # try:
        #    prov = driver.find_element(
        #        By.XPATH, f'/html/body/main/div[4]/form/div\
        # /div[2]/div/div[1]/div/div[2]/div[4]/div[3]/div[1]').text
        #    #print('6:',text)
        #    ans += ' ' + prov
        # except Exception:
        #    prov = ''
        #    pass

        # Эта часть кода для симф-москва. Проверка купе.
        if "Купе" not in ans:
            print('not ("Купе" in ans)')
            ans = ""
        #

        # if 'низ' not in ans:
        #    print('aaaaqa')
        #    ans = ''
        ###

        if seat != "любая" and seat not in ans:
            ans = ""

        # print('2ans = ', ans)
        if "Купе" not in ans and "Плац" not in ans:
            ans = ""

        print("ans = ", ans)

    print("\n", ans)
    if not CANCEL_FLAG:
        await bot.send_message(
            callback_query.from_user.id, text=messages.ticket_is_ready(url, ans)
        )
    else:
        await bot.send_message(callback_query.from_user.id, text=messages.cancel())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# было: /html/body/main/div[2]/form/div/div[2]/div/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[3]
# стало:
# /html/body/main/div[3]/form/div/div[2]/div/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[3]

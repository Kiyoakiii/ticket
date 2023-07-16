import asyncio
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6321448809:AAEompqKcjWHFP3bIn8tcV11ZpvjEct2Lr8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

cancel_flag = False

@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    global cancel_flag
    cancel_flag = False
    await message.answer("Я начинаю выполнять длительную операцию. Отправьте /cancel, чтобы остановить ее.")
    for i in range(10):
        if cancel_flag:
            await message.answer("Операция была отменена.")
            break
        await message.answer(f"Шаг {i+1} из 10")
        await asyncio.sleep(1)
    else:
        await message.answer("Операция успешно завершена.")

@dp.message_handler(commands=['cancel'])
async def cancel_cmd_handler(message: types.Message):
    global cancel_flag
    cancel_flag = True
    await message.answer("Я получил команду на отмену операции.")

if __name__ == '__main__':
    executor.start_polling(dp)

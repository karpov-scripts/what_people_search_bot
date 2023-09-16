from aiogram import Bot, Dispatcher, executor, types
import asyncio

from database import Database
from config import bot_token, admin_id, news_message_period
from messages import get_news_message, get_start_news_message


bot = Bot(token=bot_token)
dp = Dispatcher(bot)
db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Подписка на ежедневные новости оформлена!')

    news_message = get_start_news_message()
    if news_message:
        await bot.send_message(message.from_user.id, news_message, parse_mode='HTML', disable_web_page_preview=True)
        await bot.send_message(admin_id, '👏 Новый подписчик!')


@dp.message_handler(commands=['start_news'])
async def start_news(message: types.Message):
    if message.from_user.id == admin_id:
        while True:
            counter_of_subscribers = 0
            news_message = get_news_message()

            if news_message:
                users = db.get_users()
                for row in users:
                    try:
                        await bot.send_message(row[0], news_message, parse_mode='HTML', disable_web_page_preview=True)
                        counter_of_subscribers += 1
                        if int(row[1]) != 1:
                            db.set_active(row[0], 1)
                    except:
                        db.set_active(row[0], 0)

                await bot.send_message(admin_id, f'💬 Новости получили: {counter_of_subscribers} чел.')
                await asyncio.sleep(news_message_period)


@dp.message_handler(commands=['send_all'])
async def send_all(message: types.Message):
    if message.from_user.id == admin_id:
        message_for_all = message.text[9:]
        counter_of_subscribers = 0
        users = db.get_users()

        for row in users:
            try:
                await bot.send_message(row[0], message_for_all)
                counter_of_subscribers += 1
                if int(row[1]) != 1:
                    db.set_active(row[0], 1)
            except:
                db.set_active(row[0], 0)

        await bot.send_message(admin_id, f'💬 Сообщение получили: {counter_of_subscribers} чел.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
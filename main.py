from aiogram import types, executor, Dispatcher
import asyncio

from loader import bot, dp, db
from config import admin_id, newsletter_period
from messages import get_news_message
from scraper import scrape_today_news


async def start_newsletter():
    """Запуск цикла рассылки по пользователям в базе данных"""

    while True:
        scrape_today_news()

        users = db.get_users()
        for row in users:
            try:
                await bot.send_message(row[0], get_news_message(), disable_web_page_preview=True)
                if int(row[1]) != 1:
                    db.set_user_active(row[0], 1)
            except:
                db.set_user_active(row[0], 0)

        await asyncio.sleep(newsletter_period)


async def on_startup(dp: Dispatcher):
    asyncio.create_task(start_newsletter())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)

    await bot.send_message(message.from_user.id, 'Подписка на ежедневные новости оформлена!')
    await bot.send_message(message.from_user.id, get_news_message(is_start=True), disable_web_page_preview=True)
    await bot.send_message(admin_id, '👏 Новый подписчик!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

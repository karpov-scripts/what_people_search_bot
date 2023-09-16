import json
import datetime

from config import news_time
from parser import get_today_news


offset = datetime.timedelta(hours=3)
datetime.timezone(offset, name='Moscow')


def get_start_news_message():
    now = datetime.datetime.now()
    now_time = now.time()

    if now_time > news_time:
        message = f'<b>🔍Что ищут сегодня?</b>\n'
    else:
        message = f'<b>🔍Сегодняшние новости ещё не готовы. Посмотрите, что искали вчера!</b>\n'

    with open('news.json', encoding='utf8') as json_file:
        today_news = json.load(json_file)

    if today_news:
        for news in today_news:
            message += f'\n<b>◽️{news["title"]}</b>\n<i>{news["traffic"]}</i>\n<a href=\"{news["link"]}\">{news["description"]}' \
                       f'///  Подробнее в Google</a>\n'

        message += '\n<i>Важно! Вся информация получена из сервисов Google. Автор бота не несёт ответственности за ' \
                   'правдоподобность сведений. Доверять компании Google или нет – персональный выбор каждого. ' \
                   'Если вам кажется, что алгоритмы Google сработали неправильно, или же вся новость недостоверна – ' \
                   'тогда лучше перепроверьте. Ошибки могут быть.</i>'

    return message


def get_news_message():
    get_today_news()
    with open('news.json', encoding='utf8') as json_file:
        today_news = json.load(json_file)

    message = f'<b>🔍Что ищут сегодня?</b>\n'

    for news in today_news:
        message += f'\n<b>◽️{news["title"]}</b>\n<i>{news["traffic"]}</i>\n<a href=\"{news["link"]}\">{news["description"]}' \
                       f'///  Подробнее в Google</a>\n'

    message += '\n<i>Важно! Вся информация получена из сервисов Google. Автор бота не несёт ответственности за ' \
               'правдоподобность сведений. Доверять компании Google или нет – персональный выбор каждого. ' \
               'Если вам кажется, что алгоритмы Google сработали неправильно, или же вся новость недостоверна – ' \
               'тогда лучше перепроверьте. Ошибки могут быть.</i>'

    return message


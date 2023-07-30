import json
from datetime import datetime
from parser import get_today_news

hello_message = 'Подписка на ежедневные новости оформлена!'


def get_start_news_message():
    now = datetime.now()
    now_time = now.strftime('%X')

    if int(now_time[:2]) >= 18:
        message = f'<b>🔍Что ищут сегодня?</b>\n'
    else:
        message = f'<b>🔍Сегодняшние новости ещё не готовы. Посмотрите, что искали вчера!</b>\n'

    with open('news.json', encoding='utf8') as json_file:
        today_news = json.load(json_file)
        
    if not today_news:
        return None

    for news in today_news:
        message += f"\n<b>◽️{news['title']}</b>\n<i>{news['traffic']}</i>\n<a href=\"{news['link']}\">{news['description']}" \
                   f"///  Подробнее в Google</a>\n"

    message += f'\n<i>Важно! Вся информация получена из сервисов Google. Автор бота не несёт ответственности за ' \
               f'правдоподобность сведений. Доверять компании Google или нет – персональный выбор каждого. ' \
               f'Если вам кажется, что алгоритмы Google сработали неправильно, или же вся новость недостоверна – ' \
               f'тогда лучше перепроверьте. Ошибки могут быть.</i>'
    return message


def get_news_message():
    get_today_news()
    with open('news.json', encoding='utf8') as json_file:
        today_news = json.load(json_file)
        
    if not today_news:
        return None

    message = f'<b>🔍Что ищут сегодня?</b>\n'
    for news in today_news:
        message += f"\n<b>◽️{news['title']}</b>\n<i>{news['traffic']}</i>\n<a href=\"{news['link']}\">{news['description']}" \
                   f"///  Подробнее в Google</a>\n"

    message += f'\n<i>Важно! Вся информация получена из сервисов Google. Автор бота не несёт ответственности за ' \
               f'правдоподобность сведений. Доверять компании Google или нет – персональный выбор каждого. ' \
               f'Если вам кажется, что алгоритмы Google сработали неправильно, или же вся новость недостоверна – ' \
               f'тогда лучше перепроверьте. Ошибки могут быть.</i>'
    return message

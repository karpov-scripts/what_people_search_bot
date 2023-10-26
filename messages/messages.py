import datetime

from config import news_time
from loader import db


offset = datetime.timedelta(hours=3)
datetime.timezone(offset, name='Moscow')


def get_news_message(is_start=False):
    now = datetime.datetime.now()
    current_time = now.time()

    if is_start and current_time < news_time:
        message = f'<b>🔍Сегодняшние новости ещё не готовы. Посмотрите, что искали вчера!</b>\n'
    elif current_time > news_time:
        message = f'<b>🔍Что ищут сегодня?</b>\n'

    actual_news = db.get_all_news()

    for news in actual_news:
        message += f'\n<b>◽️{news[1]}</b>\n<i>{news[2]}</i>\n<a href=\"{news[4]}\">{news[3]}' \
                       f'/// Подробнее в Google</a>\n'

    message += '\n<i>Важно! Вся информация получена из сервисов Google. Автор бота не несёт ' \
               'ответственности за правдоподобность сведений. Доверять компании Google или нет ' \
               '– персональный выбор каждого. Если вам кажется, что алгоритмы Google сработали неправильно,' \
               ' или же вся новость недостоверна – тогда лучше перепроверьте. Ошибки могут быть.</i>'

    return message

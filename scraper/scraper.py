import requests
from bs4 import BeautifulSoup
from datetime import datetime

from loader import db


URL = 'https://trends.google.ru/trends/trendingsearches/daily/rss?geo=RU'


def scrape_news_info():
    request = requests.get(URL)
    src = request.text

    soup = BeautifulSoup(src, 'xml')
    all_news = soup.find_all('item')
    all_news_titles = soup.find_all('title')
    all_news_traffic = soup.find_all('ht:approx_traffic')
    all_news_description = soup.find_all('ht:news_item_title')

    return all_news, all_news_traffic, all_news_titles, all_news_description


def get_news_description(all_news_description, all_news, news_index):
    for news_description_index in range(len(all_news_description)):
        if all_news_description[news_description_index].text in all_news[news_index].text:
            news_description = all_news_description[news_description_index].text

            return news_description


def get_news_link(news_description):
    search = news_description.replace(' ', '_').replace('«', '').replace('»', '').replace('&quot;', '').replace('\u200b', '')
    return f'https://www.google.com/search?q={search}'


def scrape_today_news():
    today_date = datetime.now().strftime("%d %B")[:6]

    db.delete_all_news()
    all_news, all_news_traffic, all_news_titles, all_news_description = scrape_news_info()

    n = 0
    while True:
        if today_date in all_news[n].text and all_news_traffic[n].text not in ('2,000+', '5,000+'):
            title = all_news_titles[n + 1].text
            traffic = f'{all_news_traffic[n].text} запросов'
            description = get_news_description(all_news_description, all_news, n)
            link = get_news_link(description)

            db.add_news(title, traffic, description, link)
            n += 1
        else:
            return

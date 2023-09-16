import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


URL = 'https://trends.google.ru/trends/trendingsearches/daily/rss?geo=RU'

NEWS_TEMPLATE = {'title': None,
                 'traffic': None,
                 'description': None,
                 'link': None}


def parse_news_info():
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
    search = news_description.replace(' ', '_').replace('«', '').replace('»', '').replace('&quot;', '')
    news_link = f'https://www.google.com/search?q={search}'

    return news_link


def get_today_news():
    today_date = datetime.now().strftime("%d %B")[:6]

    today_news = []
    all_news, all_news_traffic, all_news_titles, all_news_description = parse_news_info()

    news_index = 0
    while True:
        if today_date in all_news[news_index].text and all_news_traffic[news_index].text not in ('2,000+', '5,000+'):
            news = NEWS_TEMPLATE.copy()
            news['title'] = all_news_titles[news_index + 1].text
            news['traffic'] = f'{all_news_traffic[news_index].text} запросов'
            news['description'] = get_news_description(all_news_description, all_news, news_index)
            news['link'] = get_news_link(news['description'])

            today_news.append(news)
            news_index += 1
        else:
            with open('news.json', 'w', encoding='utf8') as file:
                json.dump(today_news, file, ensure_ascii=False)

            return

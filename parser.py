import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


URL = 'https://trends.google.ru/trends/trendingsearches/daily/rss?geo=RU'
news_template = {'title': None,
                 'traffic': None,
                 'description': None,
                 'link': None}


def get_all_news():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.'
    }

    request = requests.get(URL, headers=headers)
    src = request.text
    with open('google_trends.xml', 'w', encoding='utf-8') as file:
        file.write(src)

    with open('google_trends.xml', encoding="utf8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html')
    all_news = soup.find_all('item')
    all_news_titles = soup.find_all('title')
    all_news_traffic = soup.find_all('ht:approx_traffic')
    all_news_description = soup.find_all('ht:news_item_title')
    return all_news, all_news_traffic, all_news_titles, all_news_description


def get_news_description(all_news_description, all_news, news_index):
        all_news_description_number = len(all_news_description)
        for news_description_index in range(all_news_description_number):
            if all_news_description[news_description_index].text in all_news[news_index].text:
                news_description = all_news_description[news_description_index].text
        return news_description


def get_news_link(news_description):
    search = news_description.replace(' ', '_').replace('«', '').replace('»', '').replace('&quot;', '')
    news_link = f"https://www.google.com/search?q={search}"
    return news_link


def get_today_news():
    now = datetime.now()
    today_date = now.strftime("%d %B")[:6]
    today_news = []
    all_news, all_news_traffic, all_news_titles, all_news_description = get_all_news()
    news_index = 0
    while True:
        if today_date in all_news[news_index].text and all_news_traffic[news_index].text != '2,000+' \
        and all_news_traffic[news_index].text != '5,000+':
            news = news_template.copy()
            news['title'] = all_news_titles[news_index + 1].text
            news['traffic'] = all_news_traffic[news_index].text + ' запросов'
            news['description'] = get_news_description(all_news_description, all_news, news_index)
            news['link'] = get_news_link(news['description'])
            today_news.append(news)
            news_index += 1
        else:
            with open('news.json', 'w', encoding='utf8') as file:
                json.dump(today_news, file, ensure_ascii=False)
            return

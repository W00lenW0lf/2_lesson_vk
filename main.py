import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_link_click_stats(token, key):
    payload = {"access_token": token,
               "key": key,
               "interval": "month",
               "interval_count": "1",
               'v': '5.131'}
    response = requests.get(f"https://api.vk.com/method/utils.getLinkStats", params=payload)
    response.raise_for_status()
    link_statistic_data = response.json()
    if "error" in link_statistic_data:
        return None
    else:
        stats = link_statistic_data["response"]["stats"]
        if stats:
            views = stats[0]["views"]
            return "Количество кликов за месяц:" + str(views)
        else:
            return "Нет данных о переходах."

def get_shorten_link(token, url):
    payload = {"access_token": token,
               "url": url,
               'v': '5.131'}
    response = requests.get(f"https://api.vk.com/method/utils.getShortLink", params=payload)
    response.raise_for_status()
    link_shortener_data = response.json()
    if "error" in link_shortener_data:
        return None
    else:
        return link_shortener_data["response"]["short_url"]

def is_link_shorten(url):
    return urlparse(url).netloc == "vk.cc"


def main():
    load_dotenv()
    token = os.environ["VK_SERVICE_TOKEN"]
    url = input('Введите ссылку, если она короткая то программа выдаст количество переходов по ней,'
                ' если нет - сократит:  ')
    link_length = is_link_shorten(url)
    if link_length:
        key = url.replace("https://vk.cc/", "")
        link_statistic = get_link_click_stats(token, key)
        print(link_statistic)
    else:
        short_link = get_shorten_link(token, url)
        print(short_link)


if __name__ == '__main__':
    main()

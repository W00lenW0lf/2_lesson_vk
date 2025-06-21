import requests
import os
from dotenv import load_dotenv


def get_link_click_stats(token, short_code):
    payload = {"access_token": token,
               "key": short_code,
               "interval": "month",
               "interval_count": "1",
               'v': '5.131'}
    response = requests.get(f"https://api.vk.com/method/utils.getLinkStats", params=payload)
    response.raise_for_status()
    link_statistic = response.json()
    if "error" in link_statistic:
        raise Exception(f"Ошибка VK API: {link_statistic}")
    else:
        stats = link_statistic["response"]["stats"]
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
    link_shortener = response.json()
    if "error" in link_shortener:
        raise Exception(f"Ошибка VK API: {link_shortener}")
    else:
        return link_shortener["response"]["short_url"]

def is_link_shorten(token, url):
    payload = {"access_token": token,
               "url": url,
               'v': '5.131'}
    response = requests.get(f"https://api.vk.com/method/utils.checkLink", params=payload)
    response.raise_for_status()
    link_lenght = response.json()
    if link_lenght["response"]["link"] != url:
        return True
    else:
        return False


def main():
    load_dotenv()
    token = os.environ["VK_SERVICE_TOKEN"]
    url = input('Введите ссылку, если она короткая то программа выдаст количество переходов по ней,'
                ' если нет - сократит:  ')
    if is_link_shorten(token, url):
        short_code = url.replace("https://vk.cc/", "")
        link_statistic = get_link_click_stats(token, short_code)
        print(link_statistic)
    else:
        short_link = get_shorten_link(token, url)
        print(short_link)


if __name__ == '__main__':
    main()

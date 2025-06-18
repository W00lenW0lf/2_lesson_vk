import requests
import os

TOKEN = os.environ["TOKEN"]


def link_stats(token, key):
    payload = {"access_token": token,
               "key": key,
               "interval": "month",
               "interval_count": "1",
               'v': '5.131'}
    response = requests.get(f"https://api.vk.com/method/utils.getLinkStats", params=payload)
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        link_stats_output = "Ошибка:" +  data["error"]["error_msg"]
    else:
        stats = data["response"]["stats"]
        if stats:
            views = stats[0]["views"]
            link_stats_output = "Количество кликов за неделю:" + str(views)
        else:
            link_stats_output = "Нет данных о переходах."
    return link_stats_output


def shorten_link(token, url):
    payload = {"access_token": token,
               "url": url,
               'v': '5.131'}
    response = requests.get(f"https://api.vk.com/method/utils.getShortLink", params=payload)
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        shorten_link_output = "Ошибка:" + data["error"]["error_msg"]
    else:
        shorten_link_output = data["response"]["short_url"]
    return shorten_link_output


def is_shorten_link(token, url):
    if url[0:14] == "https://vk.cc/":
        link_status = "short"
    else:
        link_status = "long"
    return link_status


def main(token):
    url = input('Введите ссылку, если она короткая то программа выдаст количество переходов по ней,'
                ' если нет - сократит:  ')
    link_status = is_shorten_link(token, url)
    if link_status == "short":
        key = url.replace("https://vk.cc/", "")
        link_statistic = link_stats(token, key)
        print(link_statistic)
    elif link_status == "long":
        short_link = shorten_link(token, url)
        print(short_link)
    else:
        print("Ссылка недействительна")


if __name__ == '__main__':
    main(TOKEN)

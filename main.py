import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'url': url,
        'v': '5.199'
        }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    if 'response' not in data:
        raise ValueError('Неверный формат ссылки')
    return data['response']['short_url']


def get_link_stats(token, key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': '5.199'
        }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    if 'response' not in data or 'stats' not in data['response']:
        raise ValueError('Нет статистики кликов')
    return data['response']['stats'][0]['views']


def is_short_link(token, key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'key': key,
        'v': '5.199'
        }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    return 'response' in data


def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    url = input('Введите ссылку: ')
    parsed = urlparse(url)
    key = parsed.path.strip('/')  # извлекаем key из ссылки
    try:
        if is_short_link(token, key):
            print('Количество просмотров:', get_link_stats(token, key))
        else:
            print('Сокращенная ссылка:', shorten_link(token, url))
    except requests.exceptions.HTTPError as error:
        print(f'Ошибка API: {error}')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка сети: {e}')
    except ValueError as error:
        print(f'Ошибка данных: {error}')
    except Exception as error:
        print(f'Неожиданная ошибка: {error}')


if __name__ == '__main__':
    main()

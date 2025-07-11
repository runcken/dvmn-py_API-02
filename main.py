import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(vk_token, url):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': vk_token,
        'url': url,
        'v': '5.199'
        }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    vk_answer = response.json()
    if 'error' in vk_answer:
        raise ValueError('Неверный формат ссылки')
    return vk_answer['response']['short_url']


def get_link_stats(vk_token, key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': vk_token,
        'key': key,
        'interval': 'forever',
        'v': '5.199'
        }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    vk_answer = response.json()
    if 'error' in vk_answer:
        raise ValueError('Нет статистики кликов')
    return vk_answer['response']['stats'][0]['views']


def is_short_link(vk_token, key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': vk_token,
        'key': key,
        'v': '5.199'
        }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    vk_answer = response.json()
    return 'response' in vk_answer


def main():
    load_dotenv()
    vk_token = os.environ['VK_ACCESS_TOKEN']
    url = input('Введите ссылку: ')
    parsed_url = urlparse(url)
    key = parsed_url.path.strip('/')  # извлекаем key из ссылки
    try:
        if is_short_link(vk_token, key):
            print('Количество просмотров:', get_link_stats(vk_token, key))
        else:
            print('Сокращенная ссылка:', shorten_link(vk_token, url))
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

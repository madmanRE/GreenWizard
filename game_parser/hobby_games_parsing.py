import requests
from bs4 import BeautifulSoup
import random
from slugify import slugify
import re
import json


def make_format_for_number_of_persons(text):
    res = ''
    for i in text:
        if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']:
            res += i
        else:
            pass
    return '-'.join(res)

categories = [3, 4, 5, 6, 7, 8, 9, 10, 11]
numers = 5
text = """
Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum.
"""
data = []
region = ['kurks', 'moscow']

for i in range(1, 6):
    base_url = requests.get(f'https://hobbygames.ru/nastolnie?page={i}&parameter_type=0').text
    soup = BeautifulSoup(base_url, 'html.parser')
    div_elements = soup.find_all('div', class_='col-lg-4 col-md-6 col-sm-6 col-xs-12')

    for div in div_elements:
        title = div.find('a', class_='name')['title']
        duration_text = div.find('div', class_='params__item time').get('title')
        age_limit = div.find('div', class_='params__item age').get('title')
        number_of_persons = div.find('div', class_='params__item players').get('title')
        x = {
            "model": "catalog.game",
            "pk": numers,
            "fields": {
                "title": title,
                "description": text,
                "slug": slugify(title),
                "image": div.find('img')['src'],
                "price": div.div['data-price']+'.00',
                "number_of_persons": make_format_for_number_of_persons(number_of_persons),
                "duration": re.search(r'\d+', duration_text).group(),
                "age_limit": int(re.search(r'\d+', age_limit).group()),
                "quantity": 1,
                "availability": True,
                "number_of_views": 0,
                "number_of_sales": 0,
                "category": random.choice(categories)
            }
        }
        data.append(x)
        numers += 1


print('============================================')
print(len(data))

with open('new.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
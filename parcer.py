import requests
from bs4 import BeautifulSoup
import csv
import os


URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept':'*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html (url, params = None ):
    r = requests.get(url, headers = HEADERS, params = params)
    return r


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagintion = soup.find_all('span', class_ = 'mhide')
    if pagintion:
        return int(pagintion[-1].get_text())
    else:
        return 1 
    

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'proposition')

    cars = []
    for item in items:
        uah_price = item.find('span', class_ = 'grey size13')
        if uah_price:
            uah_price = uah_price.get_text(strip = True)
        else:
            uah_price = 'Цену уточняйте'  

        cars.append({
            'title': item.find('div', class_ = 'proposition_title').get_text(strip = True),
            'link': HOST + item.find('a').get('href'),
            'usd_price': item.find('span', class_ = 'green').get_text(strip = True),
            'uah_price': uah_price,
            'city': item.find('svg', class_ = 'svg-i16_pin').find_next('strong').get_text(strip = True)
        })
    return cars   


def save_file (items , path):
    with open(path, 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Марка','ссылка','цена в $','цена в UAH','город',])
        for item in items:
            writer.writerow([item['title'],item['link'],item['usd_price'],item['uah_price'],item['city'],])


def parse():
    URL = input('Введите URL:')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_page_count(html.text)
        for page in range(1, pages_count + 1):
           print(f'Парсинг страницы {page} из {pages_count}...')
           html = get_html( URL, params = {'page' : page})
           cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')
        os.startfile(FILE)
        
        #cars = get_content(html.text)
    else:
        print("error")


parse()
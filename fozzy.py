import requests
from bs4 import BeautifulSoup
import db



def pages_count(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'lxml')
    num_pages = int(soup.find("nav", attrs={'class': 'pagination'}).find_all('a', attrs = {'class': 'js-search-link'})[-2].next_element.strip())
    print(f"Let's count pages. Seems there are {num_pages} pages with wines")
    return num_pages


def get_links(url):
    links = []
    pages = pages_count(url)
    for i in range(1, pages + 1):        
        res = requests.get(url,
                    params={
                        "order": "product.name.asc",
                        "page": i,
                        "ResultsPerPage": 36})
        links.append(res.url)
    return links


def get_text(url):
    r = requests.get(url)
    return r.text 


def one_wine_info(soup):
    regular_price = float(soup.find('span', {'class': 'regular-price'}).contents[0].replace(',', '.').replace(' ', '').replace('грн', ''))
    price_now = float(soup.find('span', {'class': 'product-price'})['content'])
    wine_name = soup.find('div', {'class': 'h3 product-title'}).contents[1].contents[0].replace('Вино ', '')
    wine_url = soup.find('div', {'class': 'h3 product-title'}).contents[1].attrs['href']
    discont = round(regular_price - price_now, ndigits=2)
    if discont < 0:
        discont = 0

    return wine_name, price_now, regular_price, discont, wine_url



def get_data():
    db.clear_db()
    url = 'https://fozzyshop.ua/ru/s-15/prices-drop/kategoriya-vina_belye+vina_krasnye'
    parse_links = get_links(url)

    for url in parse_links:
        print(f'Parsing url {url}...')
        text=get_text(url)
        soup = BeautifulSoup(text, 'lxml')
        wine_lst = soup.find("div", attrs={'id': 'js-product-list'})
        items = wine_lst.find_all("div", attrs={'class': 'js-product-miniature-wrapper'})
        for item in items:
            wine = one_wine_info(item)
            db.add_new_wine(*wine)
    
    print('Done')
    

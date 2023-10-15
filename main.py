import requests
from dataclasses import dataclass
#import lamoda

customer_request = input('Введите поисковый запрос: ').replace(' ', '%20')
url = 'https://www.lamoda.ru/catalogsearch/result/?q=' + customer_request + '&&submit=y&page=1'

print(url)

r = requests.get(url)
text = r.text
text = str(text)

products = []


@dataclass
class Prod:
    article: str
    brand: str
    title: str
    price: int
    discount: str
    country: str


while text.count('labels') != 1:

    begin_index = text.find('labels') + 7
    text = text[begin_index:]

    article_index = text.find('short_sku') + 12
    article = ''
    while text[article_index] != '"':
        article += text[article_index]
        article_index += 1

    brand_index = text.find('name') + 7
    brand = ''
    while text[brand_index] != '"':
        brand += text[brand_index]
        brand_index += 1

    text = text[brand_index:]

    title_index = text.find('name') + 7
    print(text[title_index-7:title_index+50])
    title = ''
    while text[title_index] != '"':
        title += text[title_index]
        title_index += 1

    price_index = text.find('"price_amount') + 15
    price = ''
    while text[price_index] != ',':
        price += text[price_index]
        price_index += 1
    price = int(price)

    discount_index = text.find('percent') + 9
    discount = ''
    if 'old_price_amount' in text[:text.find('labels')]:
        while text[discount_index] != ',':
            discount += text[discount_index]
            discount_index += 1
    else:
        discount += '0'

    product = Prod(
        article=article,
        brand=brand,
        title=title,
        price=price,
        discount=discount,
        country='None'
    )

    products.append(product)

products = sorted(products, key=lambda x: x.price)

for product in products:
    print(
        product.title,
        product.brand,
        product.price,
        product.discount,
        product.article,
    )

import requests
from openpyxl import Workbook
from dataclasses import dataclass


@dataclass
class Prod:
    article: str
    brand: str
    title: str
    price: float
    discount: str
    country: str


class Search:
    def __init__(self, request, file_name):
        self.products = []

        pages = self.__request(request)
        self.__page_turner(request, pages)

        self.__pack_to_sheet(file_name)

    def __request(self, request):
        url = 'https://www.lamoda.ru/catalogsearch/result/?q=' + request + '&&submit=y&page=1&sort=price_asc&sort=price_asc'
        r = requests.get(url)

        text = r.text
        left_bord = text.find('pages')
        right_bord = text[left_bord + 7:].find(',')

        return int(text[left_bord + 7:left_bord + 7 + right_bord])

    def __page_turner(self, request, pages):
        for i in range(1, pages+1):
            print(f'Processing of {i} page...')

            url = f'https://www.lamoda.ru/catalogsearch/result/?q={request}&&submit=y&page={i}&sort=price_asc'
            r = requests.get(url)
            text = r.text
            self.__page_handler(text)

            print(f'{i} page processed successfully!')

    def __page_handler(self, text):
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

            title_index = text.find('"name"') + 8

            title = ''
            while text[title_index] != '"':
                title += text[title_index]
                title_index += 1

            price_index = text.find('"price_amount') + 15
            price = ''
            while text[price_index] != ',':
                price += text[price_index]
                price_index += 1
            price = float(price)

            discount_index = text.find('percent') + 9
            discount = ''
            if 'old_price_amount' in text[:text.find('labels')]:
                while text[discount_index] != ',':
                    discount += text[discount_index]
                    discount_index += 1
            else:
                discount += '0'

            country = self.__get_country(article)

            product = Prod(
                article=article,
                brand=brand,
                title=title,
                price=price,
                discount=discount,
                country=country
            )

            self.products.append(product)

    def __get_country(self, article):
        return 'china'

    def __pack_to_sheet(self, file_name):
        workbook = Workbook()
        worksheet = workbook.active

        worksheet.append(
            [
                'Title',
                'Brand',
                'Price',
                'Discount',
                'Article',
                'Country'
            ]
        )

        for product in self.products:
            worksheet.append(
                [
                    product.title,
                    product.brand,
                    product.price,
                    product.discount,
                    product.article,
                    product.country
                ]
            )

        workbook.save(filename=f"{file_name}.xlsx")

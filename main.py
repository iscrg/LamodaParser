from pip._vendor import requests

customer_request = input('Введите поисковый запрос: ').replace(' ', '%20')
url = 'https://www.lamoda.ru/catalogsearch/result/?q=' + customer_request + '&&submit=y&page=1'

print(url)

r = requests.get(url)
text = r.text
text = str(text)

products_list = []

while text.count('labels') != 1:

    product = []

    begin_index = text.find('labels') + 7
    text = text[begin_index:]

    article_index = text.find('short_sku') + 12
    article = ''
    while text[article_index] != '"':
        article += text[article_index]
        article_index += 1
    product.append(article)

    brand_index = text.find('name') + 7
    brand = ''
    while text[brand_index] != '"':
        brand += text[brand_index]
        brand_index += 1
    product.append(brand)

    text = text[brand_index:]

    title_index = text.find('name') + 7
    title = ''
    while text[title_index] != '"':
        title += text[title_index]
        title_index += 1
    product.append(title)

    cost_index = text.find('"price_amount') + 15
    cost = ''
    while text[cost_index] != ',':
        cost += text[cost_index]
        cost_index += 1
    cost = int(cost)
    product.append(cost)

    discount_index = text.find('percent') + 9
    discount = ''
    if 'old_price_amount' in text[:text.find('labels')]:
        while text[discount_index] != ',':
            discount += text[discount_index]
            discount_index += 1
    else:
        discount += '0'
    product.append(discount)

    products_list.append(product)

products_list = sorted(products_list, key=lambda x: x[3])
for product in products_list:
    print(*product)

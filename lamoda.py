# Это дело пока не трогайте, в вс буду все объяснять.
import requests
import asyncio
from dataclasses import dataclass

@dataclass
class Prod:
    article: str
    brand: str
    title: str
    price: int
    discount: str
    country: str

class Search:
    def __init__(self, request, file_name):
        pass

    def __request(self):
        # Запрос на ламоду на 1 стр
        pass

    def __page_turner(self, pages):
        # Цикл по страницам от 2 до ...
        pass

    def __acticle(self, ):

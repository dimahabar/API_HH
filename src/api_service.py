import json
import sys
from abc import ABC, abstractmethod
from typing import List
import requests


class API(ABC):
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[dict]:
        pass


class HhAPI(API):
    """
    Класс HhAPI предоставляет интерфейс для взаимодействия с API hh.ru, специально разработанный
    для получения данных о вакансиях.
    Этот класс упрощает процесс отправки запросов к API и обработку ответов, предоставляя методы
    для получения информации о вакансиях.

    Атрибуты:
    - BASE_URL (str): Базовый URL для запросов к API hh.ru.
    """
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.all_vacancy = None

    def get_vacancies(self, search_query: str) -> List[dict]:
        """
        Отправляет GET-запрос к API hh.ru для получения списка вакансий
        """
        params = {
            "text": search_query,
            "area": 1,
            "per_page": 100,
            'only_with_salary': True,
        }

        try:
            response = requests.get(url=self.BASE_URL, params=params)
            r = response.status_code == 200

        except requests.exceptions.ConnectionError:
            print()
            sys.exit(f"Ошибка соединения")

        else:
            self.all_vacancy = json.loads(response.text)['items']

        if self.all_vacancy is None or len(self.all_vacancy) == 0:
            sys.exit("Некорректный поисковой запрос")

        if len(params['text']) < 1:
            sys.exit("Поисковой запрос не введен")

        return self.all_vacancy

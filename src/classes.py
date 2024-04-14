import requests
import json


class HhApi:
    """
    Класс для работы с API сервиса с вакансиями hh.ru
    """

    employers_dict = {'2ГИС': '64174',
                      'Ozon': '2180',
                      'Билайн': '4934',
                      'МТС': '3776',
                      'МегаФон': '3127',
                      'СБЕР': '3529',
                      'Банк ВТБ (ПАО)': '4181',
                      'Тинькофф': '78638',
                      'АШАН Ритейл Россия': '54979',
                      'Газпромбанк': '3388'}

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_request(self, employer_id) -> dict:
        """
        Создание запроса
        """
        params = {
            "page": 1,
            "per_page": 2,
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        response = requests.get(self.url, params=params)
        if response.status_code != 200:
            raise ValueError(f'Ошибка доступа к сайту {self.url}')
        else:
            response_data = json.loads(response.text)["items"]
        response1 = requests.get('https://api.hh.ru/employers')
        response_data1 = json.loads(response1.text)["items"]
        # print('-->>', response_data1)
        return response_data

    def get_vacancies(self):
        """
        Получение вакансий с сайта
        """
        vacancies_list = []
        for employer in self.employers_dict:
            emp_vacancies = self.get_request(self.employers_dict[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list

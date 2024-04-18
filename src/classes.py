import requests
import json
import psycopg2
from config import config


class HhApi:
    """
    Класс для работы с API сервиса с вакансиями hh.ru.
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

    def get_request(self, employer_id):
        """
        Создание запроса.
        """
        params = {
            "page": 1,
            "per_page": 3,
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
        return response_data

    def get_employers_vacancies(self):
        """
        Получение списков работодателей и вакансий с сайта.
        """
        vacancies_list = []
        employers_list = []
        check = ''
        for employer in self.employers_dict:
            emp_vacancies = self.get_request(self.employers_dict[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'id_vacancy': vacancy['id'], 'url': vacancy['alternate_url'], 'salary': salary,
                     'name_vacancy': vacancy['name'], 'id_employer': vacancy["employer"]["id"]})
                if check != vacancy['employer']['id']:
                    employers_list.append(
                        {'id_employer': vacancy['employer']['id'], 'name_employer': vacancy['employer']['name']})
                    check = vacancy['employer']['id']
        return employers_list, vacancies_list


class DBManager:
    """
    Класс для подключения к БД PostgreSQL и получения результатов по различным запросам.
    """
    def __init__(self, database_name):
        self.database_name = database_name

    def execute_total(self, query):
        conn = psycopg2.connect(dbname=self.database_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        results = self.execute_total('SELECT employers.name_employer, COUNT(vacancies.id_vacancy) AS count_vacancies '
                                     'FROM employers '
                                     'LEFT JOIN vacancies ON employers.id_employer = vacancies.id_employer '
                                     'GROUP BY employers.name_employer ')
        return results

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        pass

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass

    def get_vacancies_with_keyword(self):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        pass

import psycopg2
from typing import Any


def create_database(database_name: str, params: dict):
    """
    Создание базы данных
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()


def create_tables(database_name: str, params: dict):
    """
    Создание таблиц в БД
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR UNIQUE NOT NULL
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    company_id INT REFERENCES employers(company_id),
                    vacancy_name TEXT NOT NULL,
                    salary INT,
                    vacancy_url VARCHAR NOT NULL
                )
            """)
    conn.commit()
    conn.close()


def save_data_to_database(database_name, employers, vacancies, params: dict):
    """
    Сохранение данных о работодателях и вакансиях в базу данных.
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cursor:
        for vacancy in vacancies:
            print('***vacancies->', vacancies)
            print('***vacancy->', vacancy)
            print("***vacancy['employer']->", vacancy['employer'])
            cursor.execute(
                """
                INSERT INTO employers (company_name)
                VALUES (%s)
                RETURNING company_id
                """,
                (vacancy['employer']))
            # company_id = cur.fetchone()[0]
    # with conn.cursor() as cur:
    #     for employer in employers:
    #         # print('emp--->', employer)
    #         cur.execute(f"INSERT INTO employers(company_name) values ('{employer}')")
    #         for vacancy in vacancies:
    #             # print('vac--->', vacancy)
    #             cur.execute(f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
    #                         f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
    #                         f"'{vacancy['employer']}', '{vacancy['url']}')")

    cursor.close()
    conn.close()

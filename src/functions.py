import psycopg2


def create_database(database_name: str, params: dict):
    """
    Создание базы данных.
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
    Создание таблиц в БД.
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                           CREATE TABLE employers (
                           id_employer INT PRIMARY KEY,
                           name_employer VARCHAR(255) UNIQUE NOT NULL
                           )
                        """)
            cur.execute("""
                           CREATE TABLE vacancies (
                           id_vacancy INT PRIMARY KEY,
                           name_vacancy VARCHAR(255) NOT NULL,
                           salary INT,
                           url VARCHAR(255),
                           id_employer INT REFERENCES employers(id_employer) NOT NULL
                           )
                        """)
    conn.close()


def save_data_to_database(database_name, employers, vacancies, params: dict):
    """
    Сохранение данных о работодателях и вакансиях в базу данных.
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("""
                               INSERT INTO employers 
                               VALUES (%s, %s)
                            """,
                            (employer["id_employer"], employer["name_employer"]))
            for vacancy in vacancies:
                cur.execute("""
                               INSERT INTO vacancies 
                               VALUES (%s, %s, %s, %s, %s)
                            """,
                            (vacancy["id_vacancy"], vacancy["name_vacancy"], vacancy["salary"], vacancy["url"],
                             vacancy["id_employer"]))

    conn.close()

import psycopg2


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
    Создание базы таблиц в БД
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR UNIQUE
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL,
                    vacancy_name TEXT NOT NULL,
                    salary INT,
                    company_name TEXT REFERENCES employers(company_name) NOT NULL,
                    vacancy_url VARCHAR NOT NULL,
                    foreign key(company_name) references employers(company_name)
                )
            """)
    conn.commit()
    conn.close()

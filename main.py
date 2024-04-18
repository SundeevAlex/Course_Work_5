from src.classes import DBManager
from src.classes import HhApi
from config import config
from src.functions import create_database, create_tables, save_data_to_database

DB_NAME = 'hh_vacancies'  # имя создаваемой БД в PostgreSQL


def main():

    response = HhApi()
    employers_vacancies_all = response.get_employers_vacancies()

    create_database(DB_NAME, config())

    create_tables(DB_NAME, config())

    save_data_to_database(DB_NAME, employers_vacancies_all[0], employers_vacancies_all[1], config())

    db = DBManager(DB_NAME)
    print(db.get_companies_and_vacancies_count())
    # print(db.get_all_vacancies())
    # print(db.get_avg_salary())
    # print(db.get_vacancies_with_higher_salary())
    # print(db.get_vacancies_with_keyword("ст"))
    # for el in db.get_vacancies_with_keyword("ст"):
    #     print(f"{el}")


if __name__ == '__main__':
    main()

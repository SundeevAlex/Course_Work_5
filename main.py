from src.classes import HhApi
from config import config
from src.functions import create_database, create_tables


def main():
    response = HhApi()
    employers_dict = response.employers_dict
    employers_all_vacancies = response.get_vacancies()
    print(employers_all_vacancies)

    params = config()
    create_database('hh_vacancies', params)

    create_tables('hh_vacancies', params)


if __name__ == '__main__':
    main()

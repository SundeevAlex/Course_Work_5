from src.classes import HhApi
from config import config
from src.functions import create_database, create_tables, save_data_to_database


def main():
    response = HhApi()
    employers_all_vacancies = response.get_vacancies()
    # employers_dict = employers_all_vacancies[0]
    # vacancies_dict = employers_all_vacancies[1]
    # print(vacancies_dict)
    # print('***************************')
    # print(employers_dict)

    params = config()
    # create_database('hh_vacancies', params)

    # create_tables('hh_vacancies', params)

    # save_data_to_database('hh_vacancies', employers_all_vacancies[0], employers_all_vacancies[1], params)


if __name__ == '__main__':
    main()

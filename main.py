from src.classes import HhApi


def main():
    response = HhApi()
    employers_dict = response.employers_dict
    employers_all_vacancies = response.get_vacancies()
    print(employers_all_vacancies)


if __name__ == '__main__':
    main()

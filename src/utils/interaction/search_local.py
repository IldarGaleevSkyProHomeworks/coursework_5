from src.abstractions.db_manager_abstract import DBManagerAbstract
from src.entities.vacancy import Vacancy
from src.utils.console_color import FG_RED, FG_RESET, FG_GREEN, FG_MAGENTA
from src.utils.interaction.utils import user_choice


def print_vacancies(vacancies: list[Vacancy]):
    if not vacancies:
        print("Нет результатов!")

    vacancies = sorted(vacancies, reverse=True)

    col_size = [
        max([len(v.title) for v in vacancies]),
        15,
        15,
        max([len(v.url) for v in vacancies]),
        max([len(v.city) for v in vacancies]),
        max([len(v.company) for v in vacancies]),
    ]

    # == Table header ==
    h_line = '-' * (sum(col_size) + len(col_size) * 2 + 2) + '\n'

    result = ''
    result += (f'{FG_MAGENTA}'
               f'{"Title": >{col_size[0]}} | '
               f'{"Salary from": <{col_size[1]}} | '
               f'{"Salary to": <{col_size[2]}} | '
               f'{"URL": <{col_size[3]}} | '
               f'{"City": <{col_size[4]}} | '
               f'{"Employer": <{col_size[5]}}'
               f'{FG_RESET}\n')
    result += h_line

    # == Table rows ==

    for vacancy in vacancies:
        result += (f'{vacancy.title: >{col_size[0]}} | '
                   f'{"-" if vacancy.salary is None or vacancy.salary.salary_from is None else str(vacancy.salary.salary_from): <{col_size[1]}} | '
                   f'{"-" if vacancy.salary is None or vacancy.salary.salary_to is None else str(vacancy.salary.salary_to): <{col_size[2]}} | '
                   f'{vacancy.url: <{col_size[3]}} | '
                   f'{vacancy.city: <{col_size[4]}} | '
                   f'{vacancy.company: <{col_size[5]}}'
                   f'\n')
    result += h_line + '\n'

    print(result)


def search_local(db_manager: DBManagerAbstract):
    while True:
        choice = user_choice(
            [
                "Вывести список всех вакансий",
                "Поиск по ключевым словам",
                "Вывести вакансии с высокой зарплатой",
                "Вывести среднюю зарплату",
                "Вывести количество вакансий и компаний",
                "Выход"
            ]
        )

        try:
            match choice:
                case 1:
                    print_vacancies(db_manager.get_all_vacancies())
                case 2:
                    print("Введите ключевые слова через запятую")
                    keywords = input(f"{FG_GREEN}Ключевые слова{FG_RESET}: ").split(',')
                    print_vacancies(db_manager.get_vacancies_with_keyword(keywords))
                case 3:
                    print_vacancies(db_manager.get_vacancies_with_higher_salary())
                case 4:
                    print(round(db_manager.get_avg_salary(), 2))
                case 5:
                    cnt = db_manager.get_companies_and_vacancies_count()
                    print(f"{FG_GREEN}Компаний{FG_RESET}: {cnt['companies']}\n{FG_GREEN}Вакансий{FG_RESET}: {cnt['vacancies']}")
                case 6:
                    break
            print()
        except ValueError:
            print("")
        except Exception as e:
            print(f"Оооой! Ошибочка!\n{FG_RED}{e}{FG_RESET}")

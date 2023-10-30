from src.abstractions.db_manager_abstract import DBManagerAbstract
from src.abstractions.vacancy_provider import SearchResult
from src.entities.vacancy import Vacancy
from src.providers.vacancy_composer import VacancyComposer
from src.utils.console_color import FG_GREEN, FG_RESET, FG_MAGENTA, FG_RED, FG_YELLOW
from src.utils.interaction.utils import user_choice


def get_vacancy_list(data: dict[str, SearchResult], sort: bool = True) -> list[Vacancy]:
    sorted_vacancies = []
    for s_result in data.values():
        sorted_vacancies.extend(s_result.result_list)

    if sort:
        return sorted(sorted_vacancies, reverse=True)

    return sorted_vacancies


def print_table(data: dict[str, SearchResult], top_count=None) -> list[Vacancy]:
    if not data:
        print("Нет результатов!")
        return []

    vacancy_list = get_vacancy_list(data)
    vacancy_list = vacancy_list[:top_count] if top_count else vacancy_list

    col_size = [
        5,
        max([len(v.title) for v in vacancy_list]),
        15,
        15
    ]

    # == Statistic ==
    max_name_len = max([len(n) for n in data.keys()])
    total = 0
    stat = ''
    for name, res in data.items():
        total += res.total_results
        stat += f'{name: >{max_name_len}}: {res.total_results} - {res.total_pages} страниц\n'

    stat += f'{"Всего": >{max_name_len}}: {total}\n'

    # == Table header ==
    h_line = '-' * (sum(col_size) + len(col_size) * 2 + 2) + '\n'

    result = ''
    result += (f'{FG_MAGENTA}'
               f'{"ID": >{col_size[0]}} | '
               f'{"Title": >{col_size[1]}} | '
               f'{"Salary from": <{col_size[2]}} | '
               f'{"Salary to": <{col_size[3]}}'
               f'{FG_RESET}\n')
    result += h_line

    # == Table rows ==

    for index, vacancy in enumerate(vacancy_list):
        result += (f'{FG_GREEN}{index: >{col_size[0]}}{FG_RESET} | '
                   f'{vacancy.title: >{col_size[1]}} | '
                   f'{"-" if vacancy.salary is None or vacancy.salary.salary_from is None else str(vacancy.salary.salary_from): <{col_size[2]}} | '
                   f'{"-" if vacancy.salary is None or vacancy.salary.salary_to is None else str(vacancy.salary.salary_to): <{col_size[3]}}'
                   f'\n')
    result += h_line + '\n'

    # print(stat + result)
    print(result + stat)
    return vacancy_list


def search_vacancy(composer: VacancyComposer):
    def get_input(prompt: str) -> str:
        r = input(prompt + '\n(оставьте пустым по умолчанию)> ')
        print()
        return r

    def get_int(prompt: str) -> int | None:
        input_str = get_input(prompt)
        if input_str and input_str.isdigit():
            return int(input_str)

        return None

    def get_list(prompt: str) -> list | None:
        input_str = get_input(prompt)
        if input_str:
            return input_str.split(',')

        return None

    keyword = input("Введите ключевые слова для поиска\n> ")

    # providers = get_list(f"Укажите провайдеров через запятую: {', '.join(composer.provider_names)}")
    providers = None
    # per_page = get_int("Укажите максимальное число вакансий на странице")
    per_page = None
    # page_num = get_int("Укажите страницу")
    page_num = None
    # top_count = get_int("Число выводимых результатов")
    top_count = None

    search_result_list = composer.get_vacancies(
        search_text=keyword,
        per_page=per_page,
        page_num=page_num,
        providers=providers)

    return print_table(
        search_result_list,
        top_count=top_count
    )
    # return search_result_list


def save_dialog(vacancy_list: list[Vacancy], db_manager: DBManagerAbstract):
    while True:
        print("Укажите ID вакансий для сохранения через запятую")
        try:
            ids = input("> ").split(',')
            ids = set([int(i) for i in ids])
            ids = ids.intersection(set(range(len(vacancy_list))))

            db_manager.insert_vacancies([vacancy_list[i] for i in ids])
            print(f"{FG_GREEN}Вакансии сохранены!{FG_RESET}")
            break
        except ValueError:
            print(f"{FG_YELLOW}Неверный формат!{FG_RESET}")
        except Exception as e:
            print(f"Оооой! Ошибочка!\n{FG_RED}{e}{FG_RESET}")
            break


def search_online(vacancy_composer: VacancyComposer, db_manager: DBManagerAbstract):
    result = []
    choice = 1
    while True:
        print()
        match choice:
            case 1:
                result = search_vacancy(vacancy_composer)
            case 2:
                if not result:
                    print("Нет результатов для сохранения!")
                    continue
                save_dialog(result, db_manager)
            case 3:
                break
        choice = user_choice(
            [
                "поиск",
                "сохранить вакансии в базе данных",
                "выход"
            ]
        )

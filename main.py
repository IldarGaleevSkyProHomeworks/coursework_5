from src.abstractions.db_manager_abstract import DBManagerAbstract
from src.data_managers.db_manager_postgres import DBManagerPG
from src.providers.vacancy_composer import VacancyComposer
from src.providers.vacancy_provider_hh import VacancyProviderHeadHunter
from src.utils.interaction.search_local import search_local
from src.utils.interaction.search_online import search_online
from src.utils.interaction.utils import user_choice


def user_interaction(vacancy_composer: VacancyComposer, db_manager: DBManagerAbstract):
    while True:
        try:
            choice = user_choice(
                [
                    "поиск вакансий в интернете",
                    "работа с базой данных",
                    "выход",
                ]
            )
            match choice:
                case 1:
                    search_online(vacancy_composer, db_manager)
                case 2:
                    search_local(db_manager)
                case 3:
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            print("До встречи!")
            break


if __name__ == '__main__':
    user_interaction(
        VacancyComposer(
            [
                VacancyProviderHeadHunter(),
            ]
        ),
        DBManagerPG()
    )

import config
from src.abstractions.db_manager_abstract import DBManagerAbstract
from src.entities.vacancy import Vacancy
from psycopg2.sql import SQL, Placeholder

import psycopg2


class DBManagerPG(DBManagerAbstract):
    def __init__(self):
        self._conn_prop = {
            'host': config.PG_DB_HOSTNAME if config.PG_DB_HOSTNAME else 'localhost',
            'port': int(config.PG_DB_PORT) if config.PG_DB_PORT else 5432,
            'database': config.PG_DB_NAME if config.PG_DB_NAME else 'vacancy_finder',
            'user': config.PG_DB_USER if config.PG_DB_USER else 'postgres',
            'password': config.PG_DB_PASSWORD,
        }

    def _get_connection(self):
        con = psycopg2.connect(**self._conn_prop)

        return con

    def get_companies_and_vacancies_count(self):
        con = self._get_connection()
        cur = con.cursor()
        cur.execute('(select count(*) from vacancies) union (select count(*) from companies);')
        con.commit()
        r = cur.fetchall()
        con.close()
        if r:
            r = (r[0][0], r[1][0])
        else:
            r = (0, 0)
        return {'vacancies': r[0], 'companies': r[1]}

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass

    def insert_vacancies(self, vacancies: list[Vacancy]):
        con = self._get_connection()
        cur = con.cursor()

        data = [(
            vacancy.title,
            vacancy.description,
            vacancy.salary.salary_from.code if vacancy.salary.salary_from else
            vacancy.salary.salary_to.code if vacancy.salary.salary_to else 'USD',
            vacancy.salary.salary_from.value if vacancy.salary.salary_from else None,
            vacancy.salary.salary_to.value if vacancy.salary.salary_to else None,
            vacancy.provider_vacancy_id,
            vacancy.company,
            vacancy.city,
            vacancy.provider if vacancy.provider else 'Unknown',
            vacancy.url,
        ) for vacancy in vacancies]

        query = SQL("INSERT INTO vacancies "
                    "("
                    "vacancy_title,"
                    "vacancy_description,"
                    "salary_currency,"
                    "salary_from,"
                    "salary_to,"
                    "provider_vacancy_id,"
                    "company_id,"
                    "city_id,"
                    "provider_id,"
                    "vacancy_url"
                    ") "
                    "VALUES "
                    "({title},"
                    "{description},"
                    "{currency},"
                    "{salary_from},"
                    "{salary_to},"
                    "{provider_vacancy_id},"
                    "get_company({company_name}),"
                    "get_city({city}),"
                    "get_provider({provider}),"
                    "{url}"
                    ") ON CONFLICT DO NOTHING; "
                    ).format(
            title=Placeholder(),
            description=Placeholder(),
            currency=Placeholder(),
            salary_from=Placeholder(),
            salary_to=Placeholder(),
            provider_vacancy_id=Placeholder(),
            company_name=Placeholder(),
            city=Placeholder(),
            provider=Placeholder(),
            url=Placeholder(),
        )
        cur.executemany(query, data)

        con.commit()
        con.close()

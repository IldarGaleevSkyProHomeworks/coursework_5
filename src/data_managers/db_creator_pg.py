import os

import config
from src.abstractions.db_creator import DBCreator, DBCreatorProp
import psycopg2
from psycopg2 import sql


class DBCreatorPG(DBCreator):

    def __init__(self):
        super().__init__()

        app_db_hostname = config.PG_DB_HOSTNAME if config.PG_DB_HOSTNAME else 'localhost'
        app_db_port = config.PG_DB_PORT if config.PG_DB_PORT else '5432'

        app_db_user = config.PG_DB_USER if config.PG_DB_USER else 'postgres'
        app_db_password = config.PG_DB_PASSWORD
        app_db_name = config.PG_DB_NAME if config.PG_DB_NAME else 'vacancy_finder'

        self._db_props['username'] = DBCreatorProp(
            'Database admin username',
            'postgres'
        )

        self._db_props['password'] = DBCreatorProp(
            'Database admin password',
            None,
            secure=True,
            validate_cb=DBCreatorProp.empty_validate
        )

        self._db_props['hostname'] = DBCreatorProp(
            'Database hostname',
            app_db_hostname
        )

        self._db_props['port'] = DBCreatorProp(
            'Database port',
            app_db_port,
            validate_cb=DBCreatorProp.digit_validate
        )

        self._db_props['dbname'] = DBCreatorProp(
            'Database name',
            app_db_name
        )

        self._db_props['app_db_user'] = DBCreatorProp(
            'Application database username',
            app_db_user,
            validate_cb=DBCreatorProp.not_eq_validate(
                self._db_props['username'].value,
                'admin user and app user are the same!'
            )
        )

        self._db_props['app_db_password'] = DBCreatorProp(
            'Application database password (will be ignored if users are same)',
            app_db_password,
            secure=True,
            validate_cb=DBCreatorProp.empty_validate
        )

    def init_database(self):

        is_create_new_user = self._db_props['username'].value != self._db_props['app_db_user'].value

        user = self._db_props['app_db_user'].value
        pwd = self._db_props['app_db_password'].value if is_create_new_user else self._db_props['password'].value
        dbname = self._db_props['dbname'].value

        conn_props = {
            'host': self._db_props['hostname'].value,
            'port': int(self._db_props['port'].value),
            'database': 'postgres',
            'user': self._db_props['username'].value,
            'password': self._db_props['password'].value,
        }

        # =================== CREATE USER AND DATABASE ===================

        conn = psycopg2.connect(**conn_props)
        conn.autocommit = True
        cur = conn.cursor()

        if is_create_new_user:
            create_user = sql.SQL('CREATE USER {user} WITH PASSWORD {password};').format(
                user=sql.Identifier(user),
                password=sql.Literal(pwd)
            )
            cur.execute(create_user)

        create_db = sql.SQL('CREATE DATABASE {dbname} WITH OWNER = {user};').format(
            dbname=sql.Identifier(dbname),
            user=sql.Identifier(user)
        )
        cur.execute(create_db)

        if is_create_new_user:
            create_grant = sql.SQL('GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {user};').format(
                dbname=sql.Identifier(dbname),
                user=sql.Identifier(user)
            )
            cur.execute(create_grant)

        conn.close()

        # =================== CREATE TABLES =================

        conn_props['database'] = dbname
        conn_props['user'] = user
        conn_props['password'] = pwd

        conn = psycopg2.connect(**conn_props)
        cur = conn.cursor()

        # ==== TABLE:COMPANIES ====
        create_table_companies = sql.SQL('CREATE TABLE public.companies ('
                                         'company_id serial,'
                                         'company_name varchar(100),'
                                         'PRIMARY KEY (company_id));'
                                         )
        cur.execute(create_table_companies)

        # ==== TABLE:CITIES ====
        create_table_cities = sql.SQL('CREATE TABLE public.cities ('
                                      'city_id serial,'
                                      'city_name varchar(100) NOT NULL,'
                                      'PRIMARY KEY (city_id),'
                                      'UNIQUE (city_name));'
                                      )
        cur.execute(create_table_cities)

        # ==== TABLE:VACANCIES ====
        create_table_vacancies = sql.SQL('CREATE TABLE public.vacancies ('
                                         'vacancy_id serial,'
                                         'provider_vacancy_id integer,'
                                         'company_id integer,'
                                         'city_id integer,'
                                         'vacancy_title varchar(250),'
                                         'vacancy_url varchar(250),'
                                         'vacancy_description text,'
                                         'PRIMARY KEY (vacancy_id),'
                                         'FOREIGN KEY (city_id) REFERENCES public.cities (city_id),'
                                         'FOREIGN KEY (company_id) REFERENCES public.companies (company_id));'
                                         )
        cur.execute(create_table_vacancies)

        # ==== COMMIT ====
        conn.commit()
        conn.close()

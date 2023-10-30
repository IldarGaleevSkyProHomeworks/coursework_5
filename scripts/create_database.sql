
-----------------|TABLE: COMPANIES|--------------
CREATE TABLE public.companies (
company_id serial,
company_name varchar(100) NOT NULL,

PRIMARY KEY (company_id),

UNIQUE (company_name));

-----------------|TABLE: CITIES|--------------
CREATE TABLE public.cities (
city_id serial,
city_name varchar(100) NOT NULL,

PRIMARY KEY (city_id),

UNIQUE (city_name));

-----------------|TABLE: PROVIDERS|--------------
CREATE TABLE public.providers (
provider_id serial,
provider_name varchar(100) NOT NULL,

PRIMARY KEY (provider_id),

UNIQUE (provider_name));

-----------------|TABLE: VACANCIES|--------------
CREATE TABLE public.vacancies (
vacancy_id serial,
provider_id integer,
provider_vacancy_id integer,
company_id integer,
city_id integer,
salary_from money,
salary_to money,
salary_currency varchar(3),
vacancy_title varchar(250) NOT NULL,
vacancy_url varchar(250),
vacancy_description text,

PRIMARY KEY (vacancy_id),

FOREIGN KEY (provider_id) REFERENCES public.providers (provider_id),
FOREIGN KEY (city_id) REFERENCES public.cities (city_id),
FOREIGN KEY (company_id) REFERENCES public.companies (company_id),

UNIQUE (provider_id, provider_vacancy_id));

--------------| FUNCTION:GET_CITY |-------------
CREATE OR REPLACE FUNCTION public.get_city(IN c_name character varying)
    RETURNS integer
LANGUAGE 'plpgsql'
    VOLATILE
    PARALLEL UNSAFE
    COST 100
AS $BODY$
    declare
        c_id int;
    begin
        c_id:= (select city_id from cities where city_name=c_name);
        if c_id is null then
            insert into cities (city_name) values (c_name) returning city_id into c_id;
        end if;
        return c_id;
    end
$BODY$;

------------| FUNCTION:GET_COMPANY |------------
CREATE OR REPLACE FUNCTION public.get_company(IN c_name character varying)
    RETURNS integer
LANGUAGE 'plpgsql'
    VOLATILE
    PARALLEL UNSAFE
    COST 100
AS $BODY$
    declare
        c_id int;
    begin
        c_id:= (select company_id from companies where company_name=c_name);
        if c_id is null then
            insert into companies (company_name) values (c_name) returning company_id into c_id;
        end if;
        return c_id;
    end
$BODY$;

------------| FUNCTION:GET_PROVIDER |------------
CREATE OR REPLACE FUNCTION public.get_provider(IN p_name character varying)
    RETURNS integer
LANGUAGE 'plpgsql'
    VOLATILE
    PARALLEL UNSAFE
    COST 100
AS $BODY$
    declare
        p_id int;
    begin
        p_id:= (select provider_id from providers where provider_name=p_name);
        if p_id is null then
            insert into providers (provider_name) values (p_name) returning provider_id into p_id;
        end if;
        return p_id;
    end
$BODY$;

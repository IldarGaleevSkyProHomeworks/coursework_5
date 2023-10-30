import os

# Postgres database configuration
PG_DB_HOSTNAME = os.getenv('PG_DB_HOSTNAME')
PG_DB_PORT = os.getenv('PG_DB_PORT')

PG_DB_USER = os.getenv('PG_DB_USER')
PG_DB_PASSWORD = os.getenv('PG_DB_PASSWORD')
PG_DB_NAME = os.getenv('PG_DB_NAME')

# Postgres database initialization script
PG_DB_INIT_SCRIPT = os.path.join(os.path.dirname(__file__), 'scripts', 'create_database.sql')

# Vacancy providers user-agent string
APP_NAME = "SkyPro_Coursework5"
APP_VER = "1.0_Dev"
APP_EMAIL = "ildar-galeev92@mail.ru"

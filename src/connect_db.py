import psycopg2

from config import dbname, host, password, user


def create_database() -> None:
    """Функция для создания базы данных"""

    # подключение к базе данных
    conn = psycopg2.connect(host=host, user=user, password=password, database="postgres")
    conn.autocommit = True  # автоматическое подтверждение изменений
    cur = conn.cursor()  # открытие курсора

    try:
        # Завершаем активные подключения
        cur.execute(
            f"""
            SELECT pg_terminate_backend(pid) 
            FROM pg_stat_activity 
            WHERE datname = '{dbname}' AND pid <> pg_backend_pid();
            """
        )
        # Удаляем базу данных если она существует
        cur.execute(f"DROP DATABASE IF EXISTS {dbname};")

        # Создаем новую базу данных
        cur.execute(f"CREATE DATABASE {dbname};")
        print(f"База данных '{dbname}' успешно создана.")

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")

    finally:
        cur.close()  # закрытие курсора
        conn.close()  # закрытие соединения


def create_tables() -> None:
    """Функция для создания таблиц"""

    conn = psycopg2.connect(host=host, user=user, password=password, database=dbname)
    cur = conn.cursor()

    create_employers_table = """
    CREATE TABLE IF NOT EXISTS employers (
        id SERIAL PRIMARY KEY,
        employer_id VARCHAR(255) UNIQUE NOT NULL,
        employer_name VARCHAR(255) NOT NULL
    );
    """

    create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        name_vacancy VARCHAR(255) NOT NULL,
        salary_from INTEGER,
        salary_to INTEGER,
        link VARCHAR(255),
        employer_id VARCHAR(255) REFERENCES employers(employer_id) ON DELETE CASCADE
    );
    """

    try:
        cur.execute(create_employers_table)
        cur.execute(create_vacancies_table)
        conn.commit()
        print("Таблицы успешно созданы.")

    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

    finally:
        cur.close()
        conn.close()

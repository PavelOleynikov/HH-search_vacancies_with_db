import psycopg2

from config import dbname, host, password, user
from src.hh_api import HeadHunterAPI


def fill_tables(employer_ids: list[str]) -> None:
    """Функция заполнения таблицы данными о работодателях и их вакансиях"""

    hh_api = HeadHunterAPI()  # Создаем экземпляр класса HeadHunterAPI

    try:
        connection = psycopg2.connect(host=host, user=user, password=password, database=dbname)
        cursor = connection.cursor()
        # Очистка данных таблиц employers и vacancies со сбросом счетчика id
        cursor.execute("TRUNCATE TABLE employers, vacancies RESTART IDENTITY;")
        connection.commit()

        for employer_id in employer_ids:
            try:
                employer_data = hh_api.get_vacancies(employer_id)
                employer_id_value = employer_data[0][0]
                # Добавление данных в таблицу employers с игнорированием дубликатов
                insert_employer_query = """
                    INSERT INTO employers (employer_id, employer_name)
                    VALUES (%s, %s) ON CONFLICT (employer_id) DO NOTHING;
                """
                cursor.execute(
                    insert_employer_query,
                    (
                        employer_id_value,
                        employer_data[0][1],
                    ),
                )
                connection.commit()

                insert_vacancy_query = """
                    INSERT INTO vacancies (name_vacancy, salary_from, salary_to, link, employer_id)
                    VALUES (%s, %s, %s, %s, %s);
                """

                for vacancy in employer_data:

                    cursor.execute(
                        insert_vacancy_query,
                        (
                            vacancy[2],
                            vacancy[3],
                            vacancy[4],
                            vacancy[5],
                            employer_id_value,
                        ),
                    )

            except Exception as e:
                print(f"Ошибка при обработке id работодателя {employer_id}: {e}")

        connection.commit()
        print("Таблицы успешно заполнены данными.")

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

    finally:
        cursor.close()
        connection.close()

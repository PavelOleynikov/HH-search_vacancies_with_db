from src.connect_db import create_database, create_tables
from src.utils import fill_tables
from src.db_manager import DBManager
from config import host, user, password, dbname

# список ID компаний для заполнения таблиц
employers_ids = [
    "4181",
    "2180",
    "78638",
    "3529",
    "80",
    "3388",
    "4496",
    "7944",
    "5923",
    "586",
]


def user_interface() -> None:
    """Функция для взаимодействия с пользователем."""

    db_manager = DBManager(dbname, user, password, host)

    while True:
        print("\nВыберите запрос:")
        print("1. Получить список всех компаний и количества вакансий у каждой компании.")
        print(
            "2. Получить список всех вакансий с указанием названия компании, "
            "названия вакансии, зарплаты и ссылки на вакансию."
        )
        print("3. Получить среднюю зарплату по вакансиям.")
        print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
        print("5. Получить список всех вакансий по ключевому слову.")
        print("6. Выход.")

        choice = input("Введите номер запроса: ").strip()

        if choice == "1":
            result = db_manager.get_companies_and_vacancies_count()
            for company, count in result:
                print(f"Компания {company}: {count} вакансий")

        elif choice == "2":
            result = db_manager.get_all_vacancies()
            for company, vacancy, salary, link in result:
                print(f"{company}: {vacancy}, зарплата: {salary}, ссылка на вакансию: {link}")

        elif choice == "3":
            result = db_manager.get_avg_salary()
            for avg_salary in result:
                print(f"Средняя зарплата по вакансиям: {avg_salary} рублей")

        elif choice == "4":
            result = db_manager.get_vacancies_with_higher_salary()
            for company, vacancy, salary, link in result:
                print(f"{company}: {vacancy}, зарплата: {salary}, ссылка на вакансию: {link}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска вакансий: ").strip().lower()
            result = db_manager.get_vacancies_with_keyword(keyword)
            for company, vacancy, salary, link in result:
                print(f"{company}: {vacancy}, зарплата: {salary}, ссылка на вакансию: {link}")

        elif choice == "6":
            db_manager.close_db()
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер из меню.")


def main() -> None:
    """Функция, которая запускает программу"""

    create_database()
    create_tables()
    fill_tables(employers_ids)
    user_interface()


if __name__ == "__main__":
    main()

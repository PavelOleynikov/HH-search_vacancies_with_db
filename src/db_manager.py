import psycopg2
from typing import List, Tuple
from config import host, user, password, dbname


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(
        self,
        dbname: str = dbname,
        user: str = user,
        password: str = password,
        host: str = host,
    ) -> None:
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Метод для получения списка всех компаний и количества вакансий у каждой компании"""

        query = """
        SELECT employers.employer_name, COUNT(vacancies.id) AS vacancies_count
        FROM employers
        LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
        GROUP BY employers.employer_name
        ORDER BY vacancies_count DESC;
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, float, str]]:
        """
        Метод для получения списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """

        query = """SELECT employers.employer_name, vacancies.name_vacancy,
        vacancies.salary_from AS salary, vacancies.link
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.employer_id;
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """Метод для получения средней зарплаты по вакансиям"""

        # берет первое not null значение из salary_from и salary_to
        query = """SELECT AVG(COALESCE(salary_from, salary_to)) AS avg_salary 
        FROM vacancies;
        """
        self.cur.execute(query)
        return self.cur.fetchone()

    def get_vacancies_with_higher_salary(
        self,
    ) -> List[Tuple[str, str, float, str]]:
        """
        Метод для получения списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям
        """

        avg_salary = self.get_avg_salary()
        query = """
        SELECT employers.employer_name, vacancies.name_vacancy,
        vacancies.salary_to AS vacancies_with_higher_salary, vacancies.link
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.employer_id
        WHERE vacancies.salary_to > %s
        ORDER BY vacancies_with_higher_salary DESC;
        """
        self.cur.execute(query, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, float, str]]:
        """
        Метод для получения списка всех вакансий,
        в названии которых содержатся переданные в метод слова
        """
        # ILIKE - поиск без учета регистра
        query = """
        SELECT employers.employer_name, vacancies.name_vacancy, vacancies.salary_from, vacancies.link
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.employer_id
        WHERE vacancies.name_vacancy ILIKE %s OR employers.employer_name ILIKE %s
        ORDER BY vacancies.salary_to DESC;
        """
        self.cur.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        return self.cur.fetchall()

    def close_db(self) -> None:
        """Метод отключения от БД"""

        self.cur.close()
        self.conn.close()


# if __name__ == "__main__":
#     db_manager = DBManager()
# result = db_manager.get_companies_and_vacancies_count()
# for company, count in result:
#     print(f"{company}: {count} вакансий")
#
# result = db_manager.get_all_vacancies()
# for company, vacancy, salary, link in result:
#     print(f"{company}: {vacancy}, зарплата: {salary}, ссылка на вакансию: {link}")

# result = db_manager.get_avg_salary()
# for avg_salary in result:
#     print(f"Средняя зарплата по вакансиям: {avg_salary} рублей")

# result = db_manager.get_vacancies_with_higher_salary()
# for company, vacancy, salary, link in result:
#     print(f"{company}: {vacancy}, зарплата: {salary}, ссылка на вакансию: {link}")

# result = db_manager.get_vacancies_with_keyword("OZON")
# for company, vacancy, salary, link in result:
#     print(f"{company}: {vacancy}, зарплата: {salary}, ссылка на вакансию: {link}")
#
# db_manager.close_db()

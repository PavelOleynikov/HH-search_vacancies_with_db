import requests


class HeadHunterAPI:
    """Класс для работы с API компаний на hh.ru"""

    def __init__(self) -> None:
        self.__base_url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self, employer_id: str, per_page: int = 100) -> list:
        """
        метод получения списка вакансий по указанному id компании
        param: employer_id - id компании
        param: per_page - количество вакансий на странице (макс 100)
        """

        params = {"employer_id": employer_id, "per_page": per_page, "area": 113, "only_with_salary": True}

        try:
            response = requests.get(self.__base_url, params=params)

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            data = response.json()
            vacancies = data.get("items", [])
            vacancies_list = []

            for item in vacancies:
                employer_id = item.get("employer", {}).get("id")
                employer_name = item.get("employer", {}).get("name")
                name_vacancy = item.get("name")
                salary_from = item.get("salary", {}).get("from")
                salary_to = item.get("salary", {}).get("to")
                alternate_url = item.get("alternate_url")

                vacancy = (employer_id, employer_name, name_vacancy, salary_from, salary_to, alternate_url)
                vacancies_list.append(vacancy)

            return vacancies_list

        except ValueError as e:
            print(f"Ошибка при обработке запроса: {e}")
            return []

import requests


class HeadHunterAPI:
    """Класс для работы с API компаний на hh.ru"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies/"

    def _connect_to_api(self) -> bool:
        """приватный метод подключения к API HeadHunter"""

        response = requests.get(self.__base_url)

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"API error: {response.status_code}")

    def get_vacancies(self, employer_ids: str, per_page: int = 100) -> list[dict]:
        """
        метод получения вакансий по указанным id компаний
        param: employer_ids - id компаний
        """

        if not self._connect_to_api():
            return []

        params = {"employer_id": employer_ids, "per_page": per_page, "area": 113, "only_with_salary": True}

        try:
            response = requests.get(self.__base_url, params=params)
            data = response.json()
            vacancies = data.get("items", ["id"])
            vacancies_list = []
            for item in vacancies:
                name_company = item.get("employer", {}).get("name")
                name_vacancy = item.get("name")
                salary = item.get("salary", {}).get("from")
                alternate_url = item.get("alternate_url")
                vacancy = (name_company, name_vacancy, salary, alternate_url)
                vacancies_list.append(vacancy)
            return vacancies_list

        except ValueError as e:
            print(f"Ошибка при обработке JSON: {e}")
            return []


if __name__ == "__main__":

    search_query = input("Введите ID компании: ")

    hh_api = HeadHunterAPI()

    # Получение вакансий с hh.ru в формате JSON
    vacancies_data = hh_api.get_vacancies(search_query)
    print(vacancies_data)

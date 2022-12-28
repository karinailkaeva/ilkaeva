import multiprocessing
import statisticsReport
from pathlib import Path
import time

vacancy_name = input('Введите название профессии: ')

class PrintingStatistic:
    """
       Обрабатывает параметры вводимые пользователями: название файла, название профессии;
       печатает статистику на экран
    """
    def __init__(self, file_name):
        """
        Инициализирует класс PrintingStatistic.
        :param file_name: string: Имя обрабатываемого файла
        """
        self.file_name = file_name

    def print_data(self):
        """Печатает статистику на экран, создает таблицы, графики и отчет с данными."""
        vacancies_objects = statisticsReport.DataSet(self.file_name).vacancies_objects
        return PrintingStatistic.print_analytical_data(vacancies_objects, vacancy_name)

    @staticmethod
    def print_analytical_data(vacancies_objects, vacancy_name):
        """
        Печатает статистику зарплаты и количества вакансий по годам и городам;
        добавляет словари со статистикой в списки:
        list_analytical_dict_year, list_analytical_dict_city, list_analytical_dict_city_1
        для создания таблиц, графиков и отчета.
        :param vacancies_objects: Список с вакансиями, на основе которого создается статистика (list)
        :param vacancy_name: Название вакансии, по которой будет выбираться статистика (str)
        :return list словарей
        """
        vacancies_dict = vacancies_objects
        years = set()
        for vacancy in vacancies_dict:
            years.add(int(vacancy.published_at[:4]))
        years = list(range(min(years), max(years) + 1))

        years_salary_dictionary = {year: [] for year in years}
        years_salary_vacancy_dict = {year: [] for year in years}
        years_count_dictionary = {year: 0 for year in years}
        years_count_vacancy_dict = {year: 0 for year in years}

        area_dict = {}

        for vacancy in vacancies_dict:
            year = int(vacancy.published_at[:4])
            years_salary_dictionary[year].append(vacancy.salary.get_salary_in_rub())
            years_count_dictionary[year] += 1
            if vacancy_name in vacancy.name:
                years_salary_vacancy_dict[year].append(vacancy.salary.get_salary_in_rub())
                years_count_vacancy_dict[year] += 1
            if vacancy.area_name in area_dict:
                area_dict[vacancy.area_name].append(vacancy.salary.get_salary_in_rub())
            else:
                area_dict[vacancy.area_name] = [vacancy.salary.get_salary_in_rub()]

        years_salary_dictionary = statisticsReport.InputConect.get_years_salary_dict(years_salary_dictionary)
        years_salary_vacancy_dict = statisticsReport.InputConect.get_years_salary_dict(years_salary_vacancy_dict)

        return [years_salary_dictionary, years_count_dictionary, years_salary_vacancy_dict, years_count_vacancy_dict]


def main(file_name):
    """
    Создает объект InputConect, печатает данные и создает таблицы, графики и отчеты
    по статистике средней зарплаты и количества вакансий.
    """
    return PrintingStatistic(file_name).print_data()

def get_multiproc():
    """
    Запускает многопроцессорность выполнения обработки CSV-файлов;
    печатает статистику.
    """
    fname = [f for f in Path(input('Введите название папки: ')).glob('*.csv')]

    with multiprocessing.Pool(processes=8) as p:
        result = p.map(main, fname)
    years_salary_dictionary = {}
    years_count_dictionary = {}
    years_salary_vacancy_dict = {}
    years_count_vacancy_dict = {}
    list_dict = [years_salary_dictionary, years_count_dictionary, years_salary_vacancy_dict, years_count_vacancy_dict]
    for year in result:
        for i in range(len(year)):
            year_items = year[i].items()
            for dic in year_items:
                list_dict[i][dic[0]] = dic[1]
    print(f'Динамика уровня зарплат по годам: {years_salary_dictionary}')
    print(f'Динамика количества вакансий по годам: {years_count_dictionary}')
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {years_salary_vacancy_dict}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {years_count_vacancy_dict}')


if __name__ == '__main__':
    start_time = time.time()
    get_multiproc()
    print("--- %s seconds ---" % (time.time() - start_time))


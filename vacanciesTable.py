import csv
from datetime import datetime
from prettytable import PrettyTable, ALL

dictionary_keys = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки',
                   'experience_id': 'Опыт работы', 'premium': 'Премиум-вакансия',
                   'employer_name': 'Компания', 'salary_from': 'Нижняя граница вилки оклада',
                   'salary_to': 'Верхняя граница вилки оклада', 'salary_gross': 'Оклад указан до вычета налогов',
                   'salary_currency': 'Идентификатор валюты оклада', 'area_name': 'Название региона',
                   'published_at': 'Дата публикации вакансии', 'salary': 'Оклад'}

dictionary_experience_id = {'noExperience': 'Нет опыта', 'between1And3': 'От 1 года до 3 лет',
                            'between3And6': 'От 3 до 6 лет', 'moreThan6': 'Более 6 лет'}

dictionary_salary_currency = {'AZN': 'Манаты', 'BYR': 'Белорусские рубли', 'EUR': 'Евро',
                              'GEL': 'Грузинский лари', 'KGS': 'Киргизский сом',
                              'KZT': 'Тенге', 'RUR': 'Рубли', 'UAH': 'Гривны',
                              'USD': 'Доллары', 'UZS': 'Узбекский сум'}

currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}

dict_experience_id = {
    'noExperience': 0,
    'between1And3': 1,
    'between3And6': 2,
    'moreThan6': 3,
}

true_false = {
    'False': 'Нет',
    'True': 'Да'
}


class Vacancy:
    """
    Класс для представления вакансии.
    Attributes:
        name (str): Название вакансии
        description (str): Описание вакансии
        key_skills (list): Список с навыками
        experience_id (str): Опыт работы
        premium (str): Премиум-вакансия
        employer_name (str): Название компании
        salary (int): Средняя зарплата
        area_name (str): Название региона
        published_at (str): Дата публикации вакансии
    """
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name,
                 published_at):
        """
        Инициализирует объект Vacancy.
        Args:
            name (str): Название вакансии
            description (str): Описание вакансии
            key_skills (list): Список с навыками
            experience_id (str): Опыт работы
            premium (str): Премиум-вакансия
            employer_name (str): Название компании
            salary (str or int or float): Средняя зарплата
            area_name (str): Название региона
            published_at (str): Дата публикации вакансии
        """
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    """
    Класс для представления зарплаты.
    Attributes:
        salary_from (int): Нижняя граница вилки оклада
        salary_to (int): Верхняя граница вилки оклада
        salary_gross (str): Оклад указан до вычета налогов
        salary_currency (str): Идентификатор валюты оклада
    """
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """
        Инициализирует объект Salary.
        Args:
            salary_from (str or int or float): Нижняя граница вилки оклада
            salary_to (str or int or float): Верхняя граница вилки оклада
            salary_gross (str): Оклад указан до вычета налогов
            salary_currency (str): Идентификатор валюты оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def get_salary_in_rub(self):
        """
        Вычисляет среднюю зарплату из вилки и переводит в рубли при помощи словаря - currency_to_rub.
        :return:
            float: Средняя зарплата в рублях
        """
        return (float(self.salary_from) + float(self.salary_to)) / 2 * currency_to_rub[self.salary_currency]


class InputConect:
    """
       Обрабатывает параметры, вводимые пользователями: фильтры, сортировка, диапазон вывода, требуемые столбцы;
       печатает таблицы на экран.
    """
    def print_data(self):
        """Получает параметры, вводимые пользователями, и на их основании печатает таблицу."""
        input_params = InputConect.input_params()
        if input_params is not None:
            file_name, field, value_field, sort_param, is_reverse_sort, borders, fields = input_params
            data_set = DataSet(file_name)
            InputConect.print_table(data_set.vacancies_objects, field, value_field, sort_param, is_reverse_sort,
                                    borders, fields)

    @staticmethod
    def input_params():
        """
        Обрабатывает параметры для печати, вводимые пользователями; не допускает печать, если параметры некорректны.
        :return:
            str: Название файла; поле, по которому происходит фильтрация;
            значения поля, по которому происходит фильтрация; параметр сортировки; порядок сортировки;
            диапазон вывода; поля для печати
        """
        file_name = input('Введите название файла: ')
        filter_param = input('Введите параметр фильтрации: ')
        sort_param = input('Введите параметр сортировки: ')
        is_reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
        borders = input('Введите диапазон вывода: ')
        fields = input('Введите требуемые столбцы: ')

        if filter_param != '':
            if not ': ' in filter_param:
                print('Формат ввода некорректен')
                return
            filter_split = filter_param.split(': ')
            field = filter_split[0]
            value_field = filter_split[1]
            if field not in dictionary_keys.values():
                print('Параметр поиска некорректен')
                return
        else:
            field = ''
            value_field = ''

        if sort_param != '':
            if not sort_param in dictionary_keys.values():
                print('Параметр сортировки некорректен')
                return
            if is_reverse_sort != 'Да' and is_reverse_sort != 'Нет' and is_reverse_sort != '':
                print('Порядок сортировки задан некорректно')
                return
        return file_name, field, value_field, sort_param, is_reverse_sort, borders, fields

    @staticmethod
    def get_key(dictionary, elem):
        """
        Возвращает ключ словаря по его значению.
        :param dictionary: Словарь, из которого нужно получить ключ (dict)
        :param elem: Значение, по которому будет извлекаться ключ (str or int or float)
        :return:
            str: Ключ словаря, найденный по его значению
        """
        for key, value in dictionary.items():
            if value == elem:
                return key

    @staticmethod
    def get_borders_table(dictionary, borders):
        """
        Возращает границы для печати таблицы.
        :param dictionary: Список, к которому будут применяться границы (list)
        :param borders: Список из двух границ (list)
        :return:
            int: левая граница вывода таблицы, права граница вывода таблицы
        """
        step = borders.split()
        step_start = int(step[0]) - 1 if len(step) > 0 else 0
        step_finish = int(step[1]) - 1 if len(step) == 2 else len(dictionary)
        return  step_start, step_finish

    @staticmethod
    def get_fields_table(table, fields):
        """
        Возвращает поля для печати таблицы.
        :param table: Таблица, которая будет напечатана
        :param fields: Поля, которые будут выведены (если их нет, будут выведены все поля таблицы)
        :return:
            list: поля таблицы, которые будут напечатаны
        """
        columns = list(filter(None, fields.split(", ")))
        all_columns = ['№'] + columns if len(columns) > 0 else table.field_names
        return all_columns

    @staticmethod
    def print_table(vacancies_objects, field, value_field, sort_param, is_reverse_sort, borders, fields):
        """
        Создает и печатает таблицу на основании параметров, введенных пользователем.
        :param vacancies_objects: Список с вакансиями (list)
        :param field: Поле, по которому происходит фильтрация (str)
        :param value_field: Значение поля, по которому происходит фильтрация (str)
        :param sort_param: Параметр, по которому происходит сортировка (str)
        :param is_reverse_sort: Порядок сортировки (str)
        :param borders: Границы вывода таблицы (list)
        :param fields: Поля таблицы для печати (str)
        """
        vacancy_dictionary = vacancies_objects
        if len(vacancy_dictionary) == 0:
            print('Нет данных')
            return

        if field != '' and value_field != '':
            vacancy_dictionary = InputConect.filter_dict_vacancies(field, value_field, vacancy_dictionary)

        if sort_param != '':
            vacancy_dictionary.sort(key=InputConect.sort_dict_vacancies(sort_param), reverse=(is_reverse_sort == 'Да'))

        if len(vacancy_dictionary) == 0:
            print('Ничего не найдено')
            return

        vacancy_dictionary = InputConect.formatter(vacancy_dictionary)

        table_vacancies = PrettyTable()
        number_vacancy = 0

        for i in range(len(vacancy_dictionary)):
            number_vacancy += 1
            word_list = list(vacancy_dictionary[i].values())
            word_list = [(string, string[:100] + "...")[len(string) > 100] for string in word_list]
            word_list.insert(0, number_vacancy)
            table_vacancies.add_row(word_list)

        table_vacancies.field_names = ["№"] + list(vacancy_dictionary[0].keys())
        table_vacancies._max_width = {el: 20 for el in table_vacancies.field_names}
        table_vacancies.hrules = ALL
        table_vacancies.align = 'l'

        border = InputConect.get_borders_table(vacancy_dictionary, borders)
        columns = InputConect.get_fields_table(table_vacancies, fields)

        print(table_vacancies.get_string(start=border[0], end=border[1], fields=columns))

    @staticmethod
    def formatter(input_dictionary):
        """
        Форматирует данные, полученные из CSV файла: переводит все слова на русский, создает поле со средней зарплатой,
        преобразует дату в формат "%d.%m.%Y".
        :param input_dictionary: Первоначальный список вакансий, полученный из CSV файлы (list)
        :return:
            dict: Отформатированный список с вакансиями
        """
        dictionary = []
        for row in input_dictionary:
            new_row = {}
            for field in row.__dict__.keys():
                if type(getattr(row, field)).__name__ == 'list':
                    new_row[dictionary_keys[field]] = '\n'.join(getattr(row, field))
                elif field == 'published_at':
                    new_row[dictionary_keys[field]] = datetime.strptime(getattr(row, field),
                                                                        '%Y-%m-%dT%H:%M:%S%z').strftime("%d.%m.%Y")
                elif field[:6] == 'salary':
                    salary_from = int(float(getattr(row, 'salary').salary_from))
                    salary_to = int(float(getattr(row, 'salary').salary_to))
                    salary_currency = dictionary_salary_currency[getattr(row, 'salary').salary_currency]
                    salary_gross = getattr(row, 'salary').salary_gross
                    if salary_gross == 'True':
                        salary_gross = 'Без вычета налогов'
                    else:
                        salary_gross = 'С вычетом налогов'
                    new_row[dictionary_keys[field]] = f'{salary_from:,} - {salary_to:,} ({salary_currency})' \
                                                      f' ({salary_gross})'.replace(',', ' ')
                elif field == 'experience_id':
                    new_row[dictionary_keys[field]] = dictionary_experience_id[getattr(row, field)]
                elif getattr(row, field) in true_false:
                    new_row[dictionary_keys[field]] = true_false[getattr(row, field)]
                else:
                    new_row[dictionary_keys[field]] = getattr(row, field)
            dictionary.append(new_row)
        return dictionary


    @staticmethod
    def filter_dict_vacancies(field, value_field, vacancies_data):
        """
        Фильтрует список вакансий по определенному значению конкретного поля.
        :param field: Поле, по которому происходит фильтрация (str)
        :param value_field:  Значение этого поля, по которому происходит фильтрация (str)
        :param vacancies_data: Список вакансий, к которому применяется фильтрация (list)
        :return:
            list: Отфильтрованный по определенному значению список с вакансиями
        """
        if field in dictionary_keys.values():
            field = InputConect.get_key(dictionary_keys, field)

        if field == 'key_skills':
            value_field = value_field.split(', ')
            return list(filter(lambda row: all([value in getattr(row, field) for value in value_field]), vacancies_data))
        if field == 'salary':
            value_field = int(value_field)
            return list(filter(lambda row: int(float(getattr(row, field).salary_from)) <=
                                           value_field <= int(float(getattr(row, field).salary_to)), vacancies_data))
        if field == 'published_at':
            value_field = datetime.strptime(value_field, '%d.%m.%Y').strftime('%Y-%m-%d')
            return list(filter(lambda row: getattr(row, field).find(value_field) != -1, vacancies_data))
        if field == 'experience_id':
            value_field = InputConect.get_key(dictionary_experience_id, value_field)
            return list(filter(lambda row: getattr(row, field) == value_field, vacancies_data))
        if field == 'salary_currency':
            value_field = InputConect.get_key(dictionary_salary_currency, value_field)
            return list(filter(lambda row: getattr(row, 'salary').salary_currency == value_field, vacancies_data))
        if field == 'premium':
            value_field = InputConect.get_key(true_false, value_field)
        return list(filter(lambda row: getattr(row, field) == value_field, vacancies_data))


    @staticmethod
    def sort_dict_vacancies(sort_param):
        """
        Определяет, как будет сортироваться таблица.
        :param sort_param: Параметр сортировки, который ввел пользователь
        :return: Способ сортировки в зависимости от параматра сортировки
        """
        if sort_param in dictionary_keys.values():
            sort_param = InputConect.get_key(dictionary_keys, sort_param)

        if sort_param == 'salary':
            return lambda row: getattr(row, sort_param).get_salary_in_rub()
        if sort_param == 'key_skills':
            return lambda row: len(getattr(row, sort_param)) if type(getattr(row, sort_param)).__name__ == 'list' else 1
        if sort_param == 'experience_id':
            return lambda row: dict_experience_id[getattr(row, sort_param)]
        return lambda row: getattr(row, sort_param)



class DataSet:
    """
    Класс для получения данных из файла CSV.
    Attributes:
        file_name (str): Название CSV файла
        vacancies_objects (list): Лист с вакансиями
    """
    def __init__(self, file_name):
        """
        Инициализирует объект DataSet, получает vacancies_objects с помощью метода чтения CSV файла - csv_reader.
        Args:
            file_name (str): Название CSV файла
            vacancies_objects (list): Лист с вакансиями
        """
        self.file_name = file_name
        self.vacancies_objects = DataSet.csv_reader(file_name)

    @staticmethod
    def delete_tags(value):
        """
        Отчищает строку от тегов.
        :param value: Строка (str)
        :return:
            str: Строка, отчищенная от тегов
        """
        temp_value = ''
        while value.find('<') != - 1:
            temp_value += value[:value.find('<')]
            current_index = value.find('>') + 1
            value = value[current_index:]
        else:
            return temp_value + value

    @staticmethod
    def csv_reader(file_name):
        """
        Читает CSV файл и создает vacancy_dictionary (лист с вакансиями) с объектами Vacancy.
        :param file_name: Имя файла CSV, из которого будут читаться данные (str)
        :return:
            list: Лист с вакансиями
        """
        with open(file_name, newline='', encoding='utf-8-sig') as file:
            vacancies_csv = csv.reader(file)
            vacancy_data = [row for row in vacancies_csv]
            vacancy_keys = []
            try:
                vacancy_keys = vacancy_data.pop(0)
            except:
                print('Пустой файл')
                exit()
            vacancy_dictionary = []
            filtered_vacancy_data = [vacancy for vacancy in vacancy_data
                                     if len(vacancy) == len(vacancy_keys) and '' not in vacancy]
            for row in filtered_vacancy_data:
                dic = {}
                for i in range(len(row)):
                    elem = DataSet.delete_tags(row[i])
                    if elem.find("\n") != -1:
                        elem = elem.split('\n')
                        elem = [' '.join(x.split()) for x in elem]
                    else:
                        elem = ' '.join(elem.split())
                    dic[vacancy_keys[i]] = elem
                vacancy_dictionary.append(
                    Vacancy(dic['name'], dic['description'], dic['key_skills'], dic['experience_id'], dic['premium'],
                            dic['employer_name'], Salary(dic['salary_from'], dic['salary_to'], dic['salary_gross'],
                            dic['salary_currency']), dic['area_name'], dic['published_at']))
            return vacancy_dictionary


def main():
    """Создает объект InputConect, печатает данные в таблицу."""
    a = InputConect()
    a.print_data()
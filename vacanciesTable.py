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
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name,
                 published_at):
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
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def get_salary_in_rub(self):
        return (float(self.salary_from) + float(self.salary_to)) / 2 * currency_to_rub[self.salary_currency]


class InputConect:
    def print_data(self):
        input_params = InputConect.input_params()
        if input_params is not None:
            file_name, field, value_field, sort_param, is_reverse_sort, borders, fields = input_params
            data_set = DataSet(file_name)
            InputConect.print_table(data_set.vacancies_objects, field, value_field, sort_param, is_reverse_sort,
                                    borders, fields)

    @staticmethod
    def input_params():
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
        for key, value in dictionary.items():
            if value == elem:
                return key

    @staticmethod
    def get_borders_table(dictionary, borders):
        step = borders.split()
        step_start = int(step[0]) - 1 if len(step) > 0 else 0
        step_finish = int(step[1]) - 1 if len(step) == 2 else len(dictionary)
        return  step_start, step_finish

    @staticmethod
    def get_fields_table(table, fields):
        columns = list(filter(None, fields.split(", ")))
        all_columns = ['№'] + columns if len(columns) > 0 else table.field_names
        return all_columns

    @staticmethod
    def print_table(vacancies_objects, field, value_field, sort_param, is_reverse_sort, borders, fields):
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
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = DataSet.csv_reader(file_name)

    @staticmethod
    def delete_tags(value):
        temp_value = ''
        while value.find('<') != - 1:
            temp_value += value[:value.find('<')]
            current_index = value.find('>') + 1
            value = value[current_index:]
        else:
            return temp_value + value

    @staticmethod
    def csv_reader(file_name):
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
    a = InputConect()
    a.print_data()
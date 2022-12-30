import APISalaryCurrency
from pathlib import Path
import csv


def csv_reader_curr_date(file_name):
    """
    Создает словарь, в котором ключ - дата (год и месяц), а значение - словарь с валютами и их курсом.
    :param file_name: CSV файл с валютами и курсами в определенное время
    :return: dict: Словарь, в котором ключ - дата (год и месяц), а значение - словарь с валютами и их курсом
    """
    with open(file_name, newline='', encoding='utf-8-sig') as file:
        curr_csv = csv.reader(file)
        curr_data = [row for row in curr_csv]
        curr_keys = []
        try:
            curr_keys = curr_data.pop(0)
        except:
            print('Пустой файл')
            exit()
        curr_dict_date = {}
        for elem in curr_data:
            curr_dict = {curr_keys[i]: elem[i] for i in range(1, len(curr_keys))}
            curr_dict_date[elem[0]] = curr_dict
        return curr_dict_date

def write_to_csv(row):
    """
    Записывает полученный лист в csv-файл.
    :param row: list: Лист с информацией о вакансии
    """
    with open(f"{row.published_at[:4]}.csv", mode="a", encoding='utf-8-sig') as w_file:
        file_writer = csv.writer(w_file, delimiter=',', lineterminator="\r")
        file_writer.writerow([row.name, row.salary, row.area_name, row.published_at])

def formatter(file, curr_dict_date):
    """
    Форматирует зарплату вакансии: приводит ее к рублям и ксреднему значению.
    :param file: Файл, из которого берутся вакансии
    :param curr_dict_date: Файл, в котором собраны курсы валют за определенный промежуток времени
    """
    vacancy_dict = APISalaryCurrency.csv_reader(file)
    row = vacancy_dict[0]
    with open(f"{row.published_at[:4]}.csv", mode="a", encoding='utf-8-sig') as w_file:
        file_writer = csv.writer(w_file, delimiter=',', lineterminator="\r")
        file_writer.writerow(row.__dict__)
    n = 0
    for row in vacancy_dict:
        date = getattr(row, 'published_at')[:7]
        salary_from = float(getattr(row, 'salary').salary_from) if getattr(row, 'salary').salary_from != '' else 0
        salary_to = float(getattr(row, 'salary').salary_to) if getattr(row, 'salary').salary_to != '' else 0
        salary_currency = getattr(row, 'salary').salary_currency

        if salary_currency in curr_dict_date[date].keys() and (salary_from != 0 or salary_to != 0) and curr_dict_date[date][salary_currency] != '':
            count_not_zero = 1 if salary_from == 0 or salary_to == 0 else 2
            salary = float(round(((salary_from + salary_to) / count_not_zero) * float(curr_dict_date[date][salary_currency])))
            row.salary = salary
            write_to_csv(row)
        elif salary_currency == 'RUR' and (salary_from != 0 or salary_to != 0):
            count_not_zero = 1 if salary_from == 0 or salary_to == 0 else 2
            salary = float(int(((salary_from + salary_to) / count_not_zero)))
            row.salary = salary
            write_to_csv(row)
        else:
            row.salary = ''
            write_to_csv(row)

def get_news_files():
    """
    Запускает форматирование вакансий из файлов, лежащих в определенной папке.
    """
    curr_dict_date = csv_reader_curr_date(input('Файл с валютами: '))
    for f in Path(input('Введите название папки: ')).glob('*.csv'):
        formatter(f, curr_dict_date)

if __name__ == '__main__':
    get_news_files()
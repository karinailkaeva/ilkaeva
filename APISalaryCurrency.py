import multiprocessing
from pathlib import Path
import csv
import statisticsReport
import requests
import xmltodict
import json
import pandas as pd


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
        for row in vacancy_data:
            dic = {}
            for i in range(len(row)):
                elem = statisticsReport.DataSet.delete_tags(row[i])
                if elem.find("\n") != -1:
                    elem = elem.split('\n')
                    elem = [' '.join(x.split()) for x in elem]
                else:
                    elem = ' '.join(elem.split())
                dic[vacancy_keys[i]] = elem
            vacancy_dictionary.append(
                statisticsReport.Vacancy(dic['name'], statisticsReport.Salary(dic['salary_from'], dic['salary_to'],
                                            dic['salary_currency']), dic['area_name'], dic['published_at']))
        return vacancy_dictionary

def get_dict_currency_year(file):
    """
    Выдает частотность встречаемых валют в списке вакансий.
    :param file: Файл с вакансиями для обработки
    :return: Словарь, где ключ - валюта, значение - количество ее встречаемости
    """
    vacancy_dictionary = csv_reader(file)
    dict_sal_currency_year = {}
    for vacancy in vacancy_dictionary:
        salary_currency = vacancy.salary.__dict__['salary_currency']
        if salary_currency not in dict_sal_currency_year:
            dict_sal_currency_year[salary_currency] = 1
        else:
            dict_sal_currency_year[salary_currency] += 1
    return dict_sal_currency_year

def get_multiproc():
    """
    Запускает многопроцессорность выполнения обработки CSV-файлов;
    соединяет статистику по количеству встречаемости валют.
    :return: полный словарь с частотностью валют
    """
    fname = [f for f in Path(input('Введите название папки: ')).glob('*.csv')]
    with multiprocessing.Pool(processes=8) as p:
        result = p.map(get_dict_currency_year, fname)
    dict_sal_currency = {}
    for year in result:
        for currency in year:
            if currency not in dict_sal_currency:
                dict_sal_currency[currency] = year[currency]
            else:
                dict_sal_currency[currency] += year[currency]
    return dict_sal_currency

def get_currency_for_convert():
    """
    Отбирает валюты, встречаемость которых не менее 5000 раз, для конвертации.
    :return: Лист с названиями валют для конвертации
    """
    dic = get_multiproc()
    currencies_for_convert = []
    for curr in dic:
        if dic[curr] >= 5000 and curr != '':
            currencies_for_convert.append(curr)
    return currencies_for_convert

def get_borders_date(currencies_for_convert):
    """
    Дает крайние даты для выборки курса валют.
    :param currencies_for_convert: Лист валют для конвертации
    :return: Крайние даты для выборки курса валют
    """
    vacancy_dictionary_start = csv_reader(input('Файл самого раннего года: '))
    vacancy_dictionary_final = csv_reader(input('Файл самого позднего года: '))
    month_min = '12'
    date_min = ''
    for vacancy in vacancy_dictionary_start:
        if vacancy.salary.__dict__['salary_currency'] in currencies_for_convert:
            vacancy_date = vacancy.published_at[:7]
            vacancy_month = vacancy.published_at[5:7]
            if vacancy_month < month_min:
                month_min = vacancy_month
                date_min = vacancy_date
            elif vacancy_month == '01':
                date_min = vacancy_date
    month_max = '01'
    date_max = ''
    for vacancy in vacancy_dictionary_final:
        if vacancy.salary.__dict__['salary_currency'] in currencies_for_convert:
            vacancy_date = vacancy.published_at[:7]
            vacancy_month = vacancy.published_at[5:7]
            if vacancy_month > month_max:
                month_max = vacancy_month
                date_max = vacancy_date
            elif vacancy_month == '12':
                date_max = vacancy_date
    return date_min, date_max

def get_val_curs():
    """
    Создает DataFrame с курсами валют (по отношению к рублю) и сохраняет его в формат .csv.
    """
    currencies_for_convert = get_currency_for_convert()
    date_min, date_max = get_borders_date(currencies_for_convert)
    currencies_date = []
    for i in range(int(date_min[:4]), int(date_max[:4]) + 1):
        for j in range(int(date_min[5:7]), 13):
            date_cur = {}
            date_cur['date'] = f'{i}-{j:02}'
            url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{j:02}/{i}'
            response = requests.get(url).text
            json_text = json.dumps(xmltodict.parse(response))
            currencies = eval(json_text)['ValCurs']['Valute']
            for currency in currencies:
                if currency['CharCode'] in currencies_for_convert:
                    date_cur[currency['CharCode']] = round(float(currency['Value'].replace(',', '.'))/
                                                               float(currency['Nominal'].replace(',', '.')), 7)

            currencies_date.append(date_cur)
            if i == int(date_max[:4]) and j == int(date_max[5:7]):
                break
    df = pd.DataFrame(currencies_date)
    df.to_csv('currencyRate.csv', index=False)

if __name__ == '__main__':
    get_val_curs()
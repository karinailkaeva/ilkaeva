import pandas as pd
import pdfkit

def get_dataframe(file, vacancy):
    vacancies = pd.read_csv(file)
    vacancies['Год'] = vacancies['published_at'].str[:4]
    vacancies_salary = round(vacancies[['Год', 'salary']].groupby('Год').mean())
    vacancies_count = vacancies.groupby('Год')['name'].count()
    vacancy_salary = round(vacancies[vacancies['name'].str.lower().str.contains(f'{vacancy}')][['Год', 'salary']]
                           .groupby('Год').mean())
    vacancy_count = vacancies[vacancies['name'].str.lower().str.contains(f'{vacancy}')].groupby('Год')['name'].count()
    statistic_vacancies = pd.merge(vacancies_salary, vacancies_count, how='left', on='Год')
    statistic_vacancies.rename(columns={'salary': 'Средняя зарплата', 'name': 'Количество вакансий'}, inplace=True)
    statistic_vacancy = pd.merge(vacancy_salary, vacancy_count, how='left', on='Год')
    statistic_vacancy.rename(columns={'salary': f'Средняя зарплата - {vacancy}',
                                      'name': f'Количество вакансий - {vacancy}'}, inplace=True)
    statistic = pd.merge(statistic_vacancies, statistic_vacancy, how='left', on='Год').fillna(0).astype(int)\
        .reset_index(level=0)
    return statistic

def get_pdf(dataframe):
    #dataframe.to_html('statisticPandas.html', index=False)
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_file(r'C:\Users\elena\PycharmProjects\LatyntsevaElena\statisticPandas.html', 'statisticPandas.pdf',
                       configuration=config, options={"enable-local-file-access": ""})

if __name__ == '__main__':
    file = input('Введите название файла: ')
    vacancy = input('Введите название профессии: ')
    get_pdf(get_dataframe(file, vacancy))


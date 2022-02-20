import json
from pprint import pprint

from bs4 import BeautifulSoup as BS
from requests import request
from urllib import parse


class HHScraper:
    def __init__(self):
        self.base_url = "https://hh.ru"

    def vacancy(self, **kwargs):
        params = parse.urlencode(kwargs)
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        response = request('get', f'{self.base_url}/search/vacancy?{params}', headers=headers)
        dom = BS(response.text, 'html.parser')
        pager = dom.find('div', {'class': 'pager'})
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

        while True:
            vacancy_list = []
            for vacancy in vacancies:
                vacancy_data = {}
                link = vacancy.find('a')
                vacancy_data['title'] = link.text
                vacancy_data['url'] = link['href']
                solary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                vacancy_data['solary'] = solary.text.replace('\u202f', '') if solary else None
                vacancy_data['source'] = self.base_url
                vacancy_list.append(vacancy_data)
            next_button = pager.find('a', {'data-qa': 'pager-next'})
            if next_button:
                url = next_button['href']
                response = request('get', f'{self.base_url}{url}', headers=headers)
                dom = BS(response.text, 'html.parser')
                vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
                pager = dom.find('div', {'class': 'pager'})
            else:
                break
            return vacancy_list


if __name__ == "__main__":
    scrapper = HHScraper()
    vacancy = input('Введите название вакансии: ')
    pprint(scrapper.vacancy(text=vacancy))

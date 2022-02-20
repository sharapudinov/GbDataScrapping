from json import dump
from requests import request
from urllib import parse


class GitHubScraper:
    def __init__(self):
        self.base_url = "https://api.github.com"

    def get_user_repos(self, username, **kwargs):
        params = parse.urlencode(kwargs)
        return request('get', self.base_url + f'/users/{username}/repos?{params}')


if __name__ == "__main__":
    scraper = GitHubScraper()
    username = input("Введите имя пользователя: ")
    response = scraper.get_user_repos(username, type='owner', accept="application/vnd.github.v3+json")
    with open(f'{username}.json', 'w') as file:
        dump(response.json(), file)

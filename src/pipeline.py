
# Pacotes
import pandas as pd
import requests
import os
import json
import re
from dotenv import load_dotenv

# Parâmetros
load_dotenv(override=True)
access_token = os.getenv("access_token")
headers = {'X-GitHub-Api-Version': '2022-11-28','Authorization': 'Bearer' + access_token}
owner = 'amzn'
url = 'https://api.github.com'
url_formatted = f'{url}/users/{owner}/repos'

# Extração
class DadosRepositorios:
    def __init__(self):
        self.owner = owner
        self.url = url
        self.access_token = access_token
        self.headers = headers
        self.save_data = r'..\data\repos_data.csv'

    # Obter o número da última página de repositórios
    def get_last_page(self):
        response = requests.get(f'{self.url}/users/{self.owner}/repos', headers=self.headers)

        if response.status_code == 200:
            link_header = response.headers.get('Link')
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="last"' in link:
                        last_url = link.split(';')[0].strip('<>')
                        match = re.search(r'page=(\d+)', last_url)
                        if match:
                            return int(match.group(1))
        return 0
    
    # Extraindo repositórios
    def fetch_repositories(self, last_page):
        repos_list = []
        for page_num in range(1, last_page + 1):
            url_page = f'{self.url}/users/{self.owner}/repos?page={page_num}'
            try:
                response = requests.get(url_page, headers=self.headers)
                repos_list.append(response.json())
            except Exception as e:
                print(f"Erro ao buscar a página {page_num}: {e}")
                repos_list.append(None)
        return repos_list

    # Extraindo informações dos repositórios
    def extract_repo_info(self, repos_list):
        repos_name, repos_description, repos_language, repos_created_at, repos_updated_at = [], [], [], [], []

        for page in repos_list:
            if page:
                for repo in page:
                    repos_name.append(repo['name'])
                    repos_description.append(repo['description'])
                    repos_language.append(repo['language'])
                    repos_created_at.append(repo['created_at'])
                    repos_updated_at.append(repo['updated_at'])
        
        return repos_name, repos_description, repos_language, repos_created_at, repos_updated_at

    # Criando dataframe para salvar os dados
    def create_dataframe(self, repos_info):
        repos_name, repos_description, repos_language, repos_created_at, repos_updated_at = repos_info
        df_repos = pd.DataFrame({
            'repo_name': repos_name,
            'repo_description': repos_description,
            'repo_language': repos_language,
            'repo_created_at': repos_created_at,
            'repo_updated_at': repos_updated_at
        })
        return df_repos
    
    # Salvando dataframe
    def save_to_csv(self, df):
        try:
            df.to_csv(self.save_data, index=False)
            print(f'DataFrame salvo em {self.save_data}')
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")

if __name__ == "__main__":
    repos = DadosRepositorios()
    last_page = repos.get_last_page()
    repos_list = repos.fetch_repositories(last_page)
    repos_info = repos.extract_repo_info(repos_list)
    df_repos = repos.create_dataframe(repos_info)
    repos.save_to_csv(df_repos)

    print(df_repos)
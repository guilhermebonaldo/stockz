import requests
from bs4 import BeautifulSoup as bs

from unidecode import unidecode
from datetime import datetime as dt
import pytz
import pandas as pd
import os
from glob import glob

class FiisBot:

    
    def get_FIIs_names(self):
    
        # pagine lista de FIIs
        html = requests.get('https://fiis.com.br/lista-de-fundos-imobiliarios/')
        
        soup = bs(html.text, 'lxml')
        # acha os tickers
        table = soup.find('div', {'id':'items-wrapper'}).findAll('span', {'class': 'ticker'})
        # trata para pegar apenas os nomes
        self.tickers = [ticker.get_text() for ticker in table]
        
        return self.tickers




    def extract_dividends_table(self, fii_name):
        # pagina com infos dos FIIs
        html = requests.get(f'https://fiis.com.br/{fii_name.lower()}/')
        soup = bs(html.text, 'lxml')
        # tabela de dividendos
        table = soup.find('table', {'id':'last-revenues--table'})
        
        # cria lista com as linhas da tabela
        l = []
        for tr in table.find_all('tr'):
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            l.append(row)

        # transforma num dataframe
        df = pd.DataFrame(l, columns=[unidecode(col_name.get_text()) for col_name in table.find_all('th')])
        
        #seleciona colunas
        df = df[['DataBase','DataPagamento', 'Rendimento']].dropna()
        
        # trata colunas
        
        df['nomeFII'] = fii_name.upper()
        
        df['Rendimento'] = df['Rendimento'].replace('R\$ ', '', regex = True)\
                                        .replace(',', '.', regex = True)\
                                        .astype(float)

        df['DataPagamento'] = pd.to_datetime(df['DataPagamento'], format='%d/%m/%y')
        df['DataBase'] = pd.to_datetime(df['DataBase'], format='%d/%m/%y')

        
        
        return df.sort_values('DataPagamento').reset_index(drop = True)


    def make_fiis_dividends_dataframe(self):
        
        # busca nomes dos FIIS disponiveis
        fiis_names = self.get_FIIs_names()

        #cria df vazio
        self.fiis_dividends = pd.DataFrame(columns = ['DataBase', 'DataPagamento', 'Rendimento', 'nomeFII'])
        
        # pra cada FII, pega a tabela e faz o append no df geral
        self.failures = []
        print(f'FIIs buscados: {len(fiis_names)}')
        for fii in fiis_names:
            try:
                df = self.extract_dividends_table(fii)
                self.fiis_dividends = pd.concat([self.fiis_dividends, df])
            
            except: self.failures.append(fii)
                
        print(f'Falhas {len(self.failures)}: {self.failures}')
                
        return self.fiis_dividends


    def update_fiis_dividends(self):

        print('Atualizando tabela de dividendos...')
        
        # get path to Stokz project
        path_to_dividends = os.getcwd().split('Stockz')[0].replace('\\', '/') + 'Stockz/data/external/FIIs/'
        
        # get all paths of FIIs dividends tables
        div_tables = sorted(glob(path_to_dividends+'*'))
        
        # read newest version
        old_div = pd.read_parquet(div_tables[-1].replace('\\', '/'))

        new_div = self.make_fiis_dividends_dataframe()

        new_div = pd.concat([old_div, new_div])
        
        # get current timestamp
        time_now = dt.now(tz=pytz.timezone('America/Sao_Paulo')).strftime('%Y%m%d_%H%M%S')
        # establish file name
        file_name = f"FIIs_{time_now}.parquet.gzip"

        new_div = new_div.drop_duplicates().to_parquet(path_to_dividends + file_name, compression = 'gzip')
        
        print('Tabela atualizada com sucesso!')
        print(f'Nome: {file_name}')

        return True


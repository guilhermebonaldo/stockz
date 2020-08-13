import pandas as pd
import seaborn as sns
from pandas_datareader import data as web
from datetime import datetime
from matplotlib import pyplot as plt
import os
from dotenv import load_dotenv, find_dotenv
import dotenv
from glob import glob
import squarify


class Stockz(object): 
    
    def __init__(self):
        
        # read xlsx
        self.portfolio_raw  = self.read_csv()
        # make dataframe stocks on columns
        self.portfolio_pivot  = self.make_pivot_portfolio(self.portfolio_raw)
        
        # get historical prices from yahoo finance
        self.historical_prices = self.get_historical_prices(self.portfolio_pivot)
        # get ibovespa historical prices from yahoo finance
        self.start_date = self.portfolio_pivot.index.min().strftime('%Y-%m-%d')
        #print('primeira data:', self.start_date)
        self.ibov = self.get_index( '^BVSP', self.start_date)
        
        # make dataframe of historical portfolio weights
        self.portfolio_weights = self.make_portfolio_weights(self.portfolio_pivot, self.historical_prices)
        # get stocks daily gains
        self.stocks_gains = self.stocks_daily_gains(self.historical_prices)
        # weighted portfolio gains
        self.portfolio_gains = self.portfolio_daily_gains(self.portfolio_weights, self.stocks_gains)
        
        
    def read_csv(self):
        
        # get path to Stokz project
        self.path_to_stockz = os.getcwd().split('Stockz')[0].replace('\\', '/') + 'Stockz/'
        # get path to env variables
        self.dotenv_path = self.path_to_stockz + 'variables.env'
        #load env variables
        load_dotenv(self.dotenv_path)
        # get data path
        self.data_path = self.path_to_stockz + os.environ.get("data_path")
        
        print(f'Lendo o arquivo {self.data_path}')
        portfolio_raw = pd.read_excel(self.data_path).dropna(how = 'any')

        # assert if table has the right columns
        for col in ['DATA', 'TIPO', 'ATIVO', 'QTD']:
            assert col in portfolio_raw.columns , print(f'dataset nao possui a coluna {col}')
            
        # DATA to_datetime
        portfolio_raw['DATA'] = pd.to_datetime(portfolio_raw['DATA'])
            
        return portfolio_raw
    
    
    def make_pivot_portfolio(self, portfolio_raw):
                
        portfolio_pivot = portfolio_raw.copy()
        
        # multiply sotck sell count with -1
        portfolio_pivot.loc[portfolio_pivot.TIPO == 'VENDA', 'QTD'] *= -1
        # pivot tabele and make cummulative sum
        portfolio_pivot = portfolio_pivot.pivot('DATA', 'ATIVO', "QTD").cumsum()
        
        # add to pivot dates until now
        date_ini = portfolio_pivot.index.max() + pd.DateOffset(1)
        date_fin = datetime.now().strftime('%Y-%m-%d')
        date_range = pd.date_range(start = date_ini, end = date_fin )
    
        head = pd.DataFrame(portfolio_pivot.tail(1), index = date_range)
        portfolio_pivot = pd.concat([portfolio_pivot, head])

        # resample daily
        portfolio_pivot = portfolio_pivot.resample('D').first().ffill().fillna(0)
        
        # filter by todays date
        self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        portfolio_pivot = portfolio_pivot[portfolio_pivot.index < self.dt]

        return portfolio_pivot#.astype(int)
    
    
    def get_historical_prices(self, portfolio):
        
        prices = pd.DataFrame(index = portfolio.index)
        
        print('Buscando preco historico de', list(portfolio.columns))
        for i in portfolio.columns:
            prices[i] = web.DataReader(str(i)+'.SA', 
                                       data_source='yahoo', 
                                       start = portfolio.index.min().strftime('%Y-%m-%d')
                                      )['Close']
        return prices
    
    
    def get_index(self,tick, start_date):
        return web.DataReader(tick, data_source='yahoo', start=start_date)['Close']
    
    
    def make_portfolio_weights(self, portfolio, prices):
        
        portfolio_weights = prices*portfolio
        
        portfolio_weights = portfolio_weights.dropna(how = 'all').ffill()
        portfolio_weights = portfolio_weights.div(portfolio_weights.sum(axis=1), axis=0)

        return portfolio_weights
    
    
    def stocks_daily_gains(self, prices):
    
        self.daily_gains = prices.dropna(how = 'all').ffill()
        
        self.daily_gains_shift = self.daily_gains.shift(1).copy()
        self.daily_gains = (self.daily_gains - self.daily_gains_shift)/self.daily_gains

        return self.daily_gains
    
    
    def portfolio_daily_gains(self, weights, gains):
       
        return (weights * gains).sum(axis = 1)
    
    
    def plot_historical_gains(self, days_lookup):
        sns.set_style("darkgrid")
        
        # portfolio
        pg_lookup = self.portfolio_gains.tail(days_lookup).add(1)
        pg_lookup.cumprod().div(pg_lookup.iloc[0]).plot(figsize = (15,5), label = 'Carteira')

        # ibovespa
        ibov_norm = self.ibov.tail(days_lookup)
        ibov_norm = ibov_norm/ibov_norm.iloc[0]
        ibov_norm.plot(figsize = (15,5), label = 'IBOV' )

        plt.legend(fontsize = 15)

        plt.show()
        
        return True
    

    def plot_daily_gains_distribution(self, days_lookup):

        sns.set_style("darkgrid")
        plt.figure(figsize = (15,5))
        
        # Distribuição dos ganhos    
        g = self.portfolio_gains.tail(days_lookup).multiply(100)

        sns.distplot(g, kde = False)

        plt.axvline(x = g.mean(),
                    ymin = 0, 
                    ymax = 100, 
                    color = 'Red',
                    label = f'Média: {g.mean().round(2)} %'
                )

        plt.axvline(x = g.tail(1).values,
                    ymin = 0, 
                    ymax = 100,
                    color = 'Green',
                    label = f'Ultimo: {g.round(2).tail(1).values[0]} %'
                )

        plt.title(f'Ganhos diários ultimos {days_lookup} dias', fontsize = 20)
        plt.legend(fontsize = 15)
        plt.show()
        
        return True


    def plot_FIIs_dividends(self):
        path_to_dividends = self.path_to_stockz + 'data/external/FIIs/'
        div_tables = sorted(glob(path_to_dividends+'*'))
        
        # read newest version
        dividends = pd.read_parquet(div_tables[-1].replace('\\', '/'))

        div = dividends[dividends['nomeFII'].isin(self.portfolio_pivot.columns)]

        div = div.pivot('DataPagamento', 'nomeFII', "Rendimento").fillna(0)

        index = pd.DataFrame(index = self.portfolio_pivot.index)

        div = index.join(div).fillna(0)

        div = div*self.portfolio_pivot[[col for col in div.columns]]

        sns.set()
        #div.index = div.index.strftime('%m-%Y')
        ax = div.resample('M').sum().tail(13).plot(kind = 'bar', stacked = True, rot=45,figsize = (15,5))

        xtl=[item.get_text()[:10] for item in ax.get_xticklabels()]
        _=ax.set_xticklabels(xtl)

        plt.title("Dividendos mensais dos FIIs", fontsize = 20)
        plt.xlabel("Mes", fontsize = 14)
        plt.ylabel("Valor", fontsize = 14)
        plt.show()

        return True

    
    def portfolio_tree_plot(self, days_lookup):

        cum_last_return = self.stocks_gains.tail(days_lookup).add(1).cumprod().tail(1).add(-1).multiply(100).iloc[0,:]

        weights = self.portfolio_weights.tail(days_lookup).mean()

        df = pd.concat([cum_last_return,weights], axis = 1)
        df.columns = ['ganhos', 'pesos']
        df = df[df.pesos > 0].sort_values('ganhos')

        volume = df.pesos.values.tolist()
        labels = [ f'{x}\n{y}%'  for x,y in zip(df.index.values,df.ganhos.round(1).values.tolist())]
        color_list = ['#D30000' if x < 0 else '#3BB143' for x in df.ganhos.round(1).values.tolist()]

        plt.figure(figsize = (10,7))
        plt.rc('font', size=14)
        squarify.plot(sizes=volume, 
                    label=labels,
                    color=color_list,
                    alpha=0.7,
                    edgecolor="white", linewidth=3)

        plt.axis('off')

        plt.show()

        return True

    
    def descriptive_gains(self):
        invested = (self.portfolio_pivot*self.historical_prices).iloc[-1,:]
        invested = invested[invested > 0].round(2)

        invested_sum = invested.sum().round(2)
        date = invested.name.strftime("%d-%m-%Y")

        desc = pd.DataFrame(invested)
        desc.columns = ['value']
        desc['percentage'] = ((desc['value']/invested_sum)*100).round(2)

        print(f'Data: {date}')
        print(f'Soma total: {invested_sum}\n')
        print(desc.sort_values('value', ascending = False))
        
        return True

    def plot_daily_gains(self, days_lookup):
        ax = self.portfolio_gains.tail(days_lookup).multiply(100).plot(kind = 'bar', figsize = (10,5), rot=45)

        xtl=[item.get_text()[:7] for item in ax.get_xticklabels()]
        _=ax.set_xticklabels(xtl)

        plt.show()

        return True
import ccxt
from dotenv import load_dotenv
import os
import pickle
from datetime import datetime

class ConnectCoinbase():

    def __init__(self):

        load_dotenv()
        self.api_key = os.getenv('COINBASE_API_KEY')
        self.api_secret = os.getenv('COINBASE_API_SECRET')

        exchange_class = getattr(ccxt, 'coinbase')
        self.exchange = exchange_class({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True,  # this option enables built-in rate limit
        })        

        # Check if the exchange is authenticated
        if not self.exchange.checkRequiredCredentials():
            print("API credentials are incorrect or not set properly.")
            exit(1)
        
        else:
            print("API credentials verified successfully")

        self.current_datetime = datetime.utcnow()
        print("current UTC time is: {}".format(self.current_datetime))
    
    def get_balance(self):

        balance = self.exchange.fetch_balance()
        total_all_currencies = balance['total']

        for currency in total_all_currencies:
            print(currency, balance[currency])

    def get_markets(self, currency_pairs=None):

        if currency_pairs is None:
            print('No currency pairs provided, using default')
            currency_pairs = [
                'ETH/GBP',
                'BTC/GBP'
            ]

        self.exchange.load_markets()

        output_dict = {}

        for pair in currency_pairs:
            market_pair = self.exchange.markets[pair]

            output_dict[market_pair['symbol']] = {
                    'id': market_pair['id'],
                    'price': market_pair['info']['price'],
                    'base': market_pair['base'],
                    'quote': market_pair['quote']
                }
        
        print(output_dict)
            
        
if __name__ == '__main__':

    currency_pairs = [
        'ETH/GBP',
        'BTC/GBP'
    ]

    #print(ccxt.coinbasepro().describe())
    coinbase = ConnectCoinbase()
    #coinbase.get_balance()
    coinbase.get_markets(currency_pairs)
    #print(dir(ccxt.coinbase()))

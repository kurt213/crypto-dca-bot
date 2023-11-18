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
            'enableRateLimit': True,  # this option enables built-in rate limit,
            'options': {
                'createMarketBuyOrderRequiresPrice': True
            }
        })        

        # Check if the exchange is authenticated
        if not self.exchange.checkRequiredCredentials():
            print("API credentials are incorrect or not set properly.")
            exit(1)
        
        else:
            print("API credentials verified successfully")

        self.current_datetime = datetime.utcnow()
        print("current UTC time is: {}".format(self.current_datetime))
    
    def get_balance(self, save_pickle=False):

        balance = self.exchange.fetch_balance()
        total_all_currencies = balance['total']

        if save_pickle:
            self._create_pickle(balance, 'example_balance.pkl')

        for currency in total_all_currencies:
            print(currency, balance[currency])

    def get_markets(self, currency_pairs=None, save_pickle=False):

        if currency_pairs is None:
            print('No currency pairs provided, using default')
            currency_pairs = [
                'ETH/GBP',
                'BTC/GBP'
            ]

        self.exchange.load_markets()

        self.currency_market_pairs = {}

        for pair in currency_pairs:
            market_pair = self.exchange.markets[pair]

            self.currency_market_pairs[market_pair['symbol']] = {
                    'id': market_pair['id'],
                    'price': market_pair['info']['price'],
                    'base': market_pair['base'],
                    'quote': market_pair['quote']
                }
        
        print(self.currency_market_pairs)
        if save_pickle:
            self._create_pickle(self.currency_market_pairs, 'example_markets.pkl')

    def get_trades(self, currency_pair=None, save_pickle=False):

        if self.exchange.has['fetchMyTrades']:
            since = self.exchange.parse8601('2023-01-01T00:00:00Z')
            all_trades = []
            while since < self.exchange.milliseconds ():
                symbol = currency_pair  # change for your symbol
                limit = 20  # change for your limit
                trades = self.exchange.fetch_my_trades(symbol, since, limit)
                if len(trades):
                    since = trades[len(trades) - 1]['timestamp'] + 1
                    all_trades += trades
                else:
                    break
            
            print(all_trades)
            if save_pickle:
                self._create_pickle(all_trades, 'example_trades.pkl')

    def create_order(self, currency_pair=None, amount_quote_currency=None, save_pickle=False):

        if self.exchange.has['createMarketOrder']:
            print("current UTC time is: {}".format(self.current_datetime))
            print('try to create market order')
            print('currency pair: {}'.format(currency_pair))
            print('amount of quote currency: {}'.format(amount_quote_currency))

            try:
                # Price is hardcoded to 1, i.e. buy x ETH at the price equivalent of 1 GBP
                order = self.exchange.create_order(currency_pair, 'market', 'buy', amount_quote_currency, 1)
                if order:
                    print("Order completed successfully")
                else:
                    print("No order output, check for failure")

                if save_pickle:
                    self._create_pickle(order, 'example_order.pkl')
                    
            except ccxt.BaseError as e:
                print('Failed to create order: {}'.format(e))

    def _create_pickle(self, data, filename):

        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        
        print('Pickle file created: {}'.format(filename))


if __name__ == '__main__':

    currency_pairs = [
        'ETH/GBP',
        'BTC/GBP'
    ]

    #print(ccxt.coinbasepro().describe())
    coinbase = ConnectCoinbase()
    #coinbase.get_balance()
    #coinbase.get_markets(currency_pairs)
    #coinbase.create_order('ETH/GBP', 1, save_pickle=False)
    coinbase.get_trades('ETH/GBP', save_pickle=False)
    #print(dir(ccxt.coinbase()))

import ccxt
from dotenv import load_dotenv
import os

class ConnectCoinbase():

    def __init__(self):

        load_dotenv()
        self.api_key = os.getenv('COINBASE_API_KEY')
        self.api_secret = os.getenv('COINBASE_API_SECRET')
    
    def connect(self):

        exchange_class = getattr(ccxt, 'coinbase')
        exchange = exchange_class({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True,  # this option enables built-in rate limit
        })        

        # Check if the exchange is authenticated
        if not exchange.checkRequiredCredentials():
            print("API credentials are incorrect or not set properly.")
            exit(1)

        # Now you can access Coinbase Pro API methods, for example, fetching your balance:
        balance = exchange.fetch_balance()
        print(balance)

if __name__ == '__main__':

    #print(ccxt.coinbasepro().describe())
    coinbase = ConnectCoinbase()
    coinbase.connect()

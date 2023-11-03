import requests
import hashlib
import hmac
import json
import time

from urllib.parse import urljoin, urlencode


class ConnectBinance():

    def __init__(self):

        # Credentials
        self.JSON_FILE = open('bot/secrets/secrets.json')
        self.SECRETS = json.load(self.JSON_FILE)

        self.API_KEY = self.SECRETS['API_KEY']
        self.SECRET_KEY = self.SECRETS['SECRET_KEY']
        self.BASE_URL = 'https://api.binance.com'

        self.HEADERS = {
            'X-MBX-APIKEY': self.API_KEY
        }

    def connect(self, query_path=None, query_params=None, test_connect=False):

        print("Connecting with standard method")

        if test_connect:
            print('Testing standard API request')
            query_path = '/api/v3/ticker/price'
            query_params = {
                'symbol': 'ETHGBP'
            }

        if query_path is None:
            print("Error: No query path parameter provided")
            return None

        url = urljoin(self.BASE_URL, query_path)

        r = requests.get(url, headers=self.HEADERS, params=query_params)

        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2))
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())        

    def connect_sig(self, query_path=None, query_params=None, generate_timestamp=True, test_connect=False):

        print("Connecting with sig method")

        if test_connect:
            print('Testing sig method API request')

            query_path = '/api/v3/order/test'
            if generate_timestamp:
                timestamp = int(time.time() * 1000)
            
            query_params = {
                'symbol': 'ETHGBP',
                'side': 'BUY',
                'type': 'MARKET',
                'timestamp': timestamp,
                'quoteOrderQty': 10,
            }

        if query_path is None:
            print("Error: No query path parameter provided")
            return None

        query_string = urlencode(query_params)
        query_params['signature'] = hmac.new(self.SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        url = urljoin(self.BASE_URL, query_path)
        r = requests.post(url, headers=self.HEADERS, params=query_params)

        if r.status_code == 200:
            data = r.json()
            print(json.dumps(data, indent=2))
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def test_connect_sapi(self, query_path, query_params, generate_timestamp=True, test_connect=False):
        
        if test_connect:
            # query_path = '/sapi/v1/capital/config/getall'
            query_path = '/sapi/v1/accountSnapshot'
            query_params = {
                'timestamp': timestamp,
                'type': 'SPOT'
            }

        if generate_timestamp:
            timestamp = int(time.time() * 1000)

        if query_path is None:
            print("Error: No query path parameter provided")
            return None

        query_string = urlencode(query_params)
        query_params['signature'] = hmac.new(self.SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        url = urljoin(self.BASE_URL, query_path)
        r = requests.get(url, headers=self.HEADERS, params=query_params)

        if r.status_code == 200:
            data = r.json()
            print(json.dumps(data, indent=2))
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())


class BinanceException(Exception):
    def __init__(self, status_code, data):

        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"

        # Python 2.x
        # super(BinanceException, self).__init__(message)
        super().__init__(message)

if __name__ == '__main__':

    print('Testing Binance API connection')

    test_auth = ConnectBinance()
    
    # This should fail and exit as there is no query_path
    test_auth.connect()

    # This should run the test connection
    test_auth.connect(test_connect=True)

    # This should run a full query connection
    test_connect_query_path = '/api/v3/ticker/price'
    test_connect_query_param =  {
        'symbol': 'BTCGBP'
    }

    test_auth.connect(test_connect_query_path, test_connect_query_param)
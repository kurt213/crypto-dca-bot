from bot import authorise_api, auth_ccxt


if __name__ == '__main__':
    
    print('start bot')

    #bot_connect = authorise_api.ConnectBinance()
    #bot_connect.connect(test_connect=True)
    coinbase = auth_ccxt.ConnectCoinbase()
    coinbase.connect()
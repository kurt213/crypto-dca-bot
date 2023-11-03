from bot import authorise_api


if __name__ == '__main__':
    
    print('start bot')

    bot_connect = authorise_api.ConnectBinance()
    bot_connect.connect(test_connect=True)

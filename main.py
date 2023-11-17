from bot import auth_ccxt
import schedule, time
import json

if __name__ == '__main__':
    
    print('start DCA bot')
    print('Connecting to Coinbase API')
    coinbase = auth_ccxt.ConnectCoinbase()

    print('Setting Schedules')
    with open('schedule.json') as f:
        schedule_data = json.load(f)
    
    for s in schedule_data:
        schedule_time = s['time']
        currency_pair = s['currency_pair']
        quote_currency_amount = s['quote_currency_amount']

        schedule.every().day.at(schedule_time).do(lambda: coinbase.create_order(currency_pair, quote_currency_amount))
        print('Schedule set: Daily at {} | Buy {} for {} source currency'.format(schedule_time, currency_pair, quote_currency_amount))

    while True:
        schedule.run_pending()
        time.sleep(60)
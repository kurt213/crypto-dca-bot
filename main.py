#!/usr/bin/env python3
from bot import auth_ccxt, scheduler
import json

if __name__ == '__main__':
    
    print('start DCA bot')
    print('Connecting to Coinbase API')
    coinbase = auth_ccxt.ConnectCoinbase()

    print('Setting Schedules')
    task_schedule = scheduler.scheduleSetup('schedule.json')

    for task in task_schedule.schedule_data:
        currency_pair = task['currency_pair']
        quote_currency_amount = task['quote_currency_amount']
        task_schedule.create_schedule(task, lambda cp=currency_pair, qca=quote_currency_amount: coinbase.create_order(cp, qca))
        #task_schedule.create_schedule(task, lambda cp=currency_pair: coinbase.get_markets(cp))

    task_schedule.show_schedule()
    task_schedule.start_schedule()

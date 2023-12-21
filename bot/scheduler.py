import schedule
import time
import json
from datetime import datetime

class scheduleSetup():
    def __init__(self, json_schedule):
        with open(json_schedule) as f:
            self.schedule_data = json.load(f)
    
        self.frequency_list = []
    
    def create_schedule(self, task, exchange):

        choice_dict = {
            'seconds': self._set_seconds,
            'hourly': self._set_hourly,
            'daily': self._set_daily,
            'weekly': self._set_weekly,
            'monthly': self._set_monthly
        }

        self.frequency_list.append(task['frequency'])

        chosen_function = choice_dict.get(task['frequency'], self._other_schedule)
        chosen_function(task, exchange)

    def _set_seconds(self, task, exchange_function):
        schedule.every(task['seconds']).seconds.do(exchange_function)
        print('Schedule set: every {} seconds | {} {} for {} source currency'.format(
            task['seconds'],
            task['buy_or_sell'],
            task['currency_pair'],
            task['quote_currency_amount']
        ))

    def _set_hourly(self, task, exchange_function):
        schedule.every().hour.do(exchange_function)
        print('Schedule set: {} | {} {} for {} source currency'.format(
            task['frequency'], 
            task['buy_or_sell'], 
            task['currency_pair'],
            task['quote_currency_amount']
        ))

    def _set_daily(self, task, exchange_function):
        schedule.every().day.at(task['time']).do(exchange_function)
        print('Schedule set: {} at {} | {} {} for {} source currency'.format(
            task['frequency'], 
            task['time'],
            task['buy_or_sell'], 
            task['currency_pair'],
            task['quote_currency_amount']
        ))

    def _set_weekly(self, task, exchange_function):
        def schedule_job(day, time):
            days = {
                'monday': schedule.every().monday,
                'tuesday': schedule.every().tuesday,
                'wednesday': schedule.every().wednesday,
                'thursday': schedule.every().thursday,
                'friday': schedule.every().friday,
                'saturday': schedule.every().saturday,
                'sunday': schedule.every().sunday
            }
            if day.lower() in days:
                days[day.lower()].at(time).do(exchange_function)
            else:
                print("Invalid day of the week")
        
        schedule_job(task['day_of_week'], task['time'])

        print('Schedule set: {} on {} at {} | {} {} for {} source currency'.format(
            task['frequency'],
            task['day_of_week'], 
            task['time'],
            task['buy_or_sell'], 
            task['currency_pair'],
            task['quote_currency_amount']
        ))
    
    def _set_monthly(self, task, exchange_function):
        def monthly_job():
            today = datetime.today()
            if today.day == task['day_of_month']:
                exchange_function()
        
        schedule.every().day.at(task['time']).do(monthly_job)

        print('Schedule set: {} on day {} at {} | {} {} for {} source currency'.format(
            task['frequency'],
            task['day_of_month'], 
            task['time'],
            task['buy_or_sell'], 
            task['currency_pair'],
            task['quote_currency_amount']
        ))

    def _other_schedule(self, task, exchange_function):
        print('no valid "frequency" key:value in schedule configuration found')

    def show_schedule(self):
        print('Scheduled jobs:')
        for job in schedule.jobs:
            print(job)

    def start_schedule(self):

        if 'hourly' in self.frequency_list or 'seconds' in self.frequency_list:
            sleep_time = 1
            print('hourly or less frequent schedule exists')
            print('set sleep time to 1 second')
        else:
            sleep_time = 60
            print('more frequent than hourly schedules only')
            print('set sleep time to 60 seconds')
        
        print('*** start schedule ***')
        while True:
            schedule.run_pending()
            time.sleep(sleep_time)


if __name__ == '__main__':

    def dummy_function(arg_1):
        print('dummy function')
        current_datetime = datetime.utcnow()
        print("current UTC time is: {}".format(current_datetime))        
        print(arg_1)

    task_schedule = scheduleSetup('schedule_template.json')

    for task in task_schedule.schedule_data:
        currency_pair = task['currency_pair']
        quote_currency_amount = task['quote_currency_amount']
        task_schedule.create_schedule(task, lambda: dummy_function('test_arg'))

    task_schedule.show_schedule()
    task_schedule.start_schedule()
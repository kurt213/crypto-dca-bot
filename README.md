# crypto-dca-bot

Tool to automate scheduled cryptocurrency purchases on Binance & Coinbase Pro. 

Frequently used for DCA (Dollar-Cost Averaging) investment strategies.

## Plan

1. Setup API for either Binance or Coinbase Pro
2. CLI for setting frequency, amount, source currency, target currency
3. Script scheduling
4. Basic UI to show transactions made

## Script Process

1. Connect - test to get list of transactions
2. Check history and balance of ETH in account
3. If last historic transactionw was at least 1 week ago - start next step
4. Execute a trade of £x amount

- Run a cron job to check this weekly 

- Will also need a logging file - recording time of check, and what happened i.e. did I buy, old, new amount, time stamp, what currency and how much

## Notes

- Originally started working on Binance and connecting to their APIs, but due to some personal consumer issues I've had with them, will be switching focus to Coinbase Pro.

## Guide

1. Create a `.env` file in the root directory of the project and add the following variables:

```
COINBASE_API_KEY=
COINBASE_API_SECRET=
```

2. Rename or copy the `schedule_template.json` to `schedule.json` and add your schedule details.

The time set is in 24 hour format and is in UTC time.

**NOTE:** Weekly frequency functionality currently not implemented. Only daily schedule available.

```
[
    {
        "frequency": "daily",
        "day_of_week": null,
        "time": "10:30",
        "currency_pair": "ETH/GBP",
        "quote_currency_amount": 1
    },
    {
        "frequency": "weekly",
        "day_of_week": "wednesday",
        "time": "15:45",
        "currency_pair": "BTC/GBP",
        "quote_currency_amount": 1
    }
]
```

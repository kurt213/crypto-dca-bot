# crypto-dca-bot

Tool to automate scheduled cryptocurrency purchases on Coinbase Advanced Trader (Previously branded as Coinbase Pro). 

Frequently used for DCA (Dollar-Cost Averaging) investment strategies.

I used to buy crypto on a weekly basis, but I found the mainstream providers charged a lot of fees for this service. I wanted to automate this process and reduce the fees I was paying by executing these trades through their trade platforms instead which have much lower fees.

## Notes

- Originally started working on Binance and connecting to their APIs, but due to some personal consumer issues I've had with them, will be switching focus to Coinbase Advanced Trader.

## Guide

This guide assumes you have some knowledge of setting up a Python environment and running Python scripts.

1. Create a Coinbase account and generate an API key & secret with the following permissions:
```
wallet:accounts:read
wallet:buys:create
wallet:orders:read
wallet:transactions:read
wallet:user:read
```

2. Create a `.env` file in the root directory of the project and add the following variables with these API details:

```
COINBASE_API_KEY=
COINBASE_API_SECRET=
```

3. Rename or copy the `schedule_template.json` to `schedule.json` and add your schedule details.

The time set is in 24 hour format and is based on the local time of the machine running the script.

**NOTE:** Currently, you can only schedule market order BUY side transactions e.g. `BTC/GBP` means you are buying `BTC` with the `quote_currency_amount` of `GBP`.

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

3. Run `main.py` script.
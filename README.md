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

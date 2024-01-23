# oatmeal

[![Portfolio](https://github.com/damiandiaz212/oatmeal/actions/workflows/portfolio.yml/badge.svg)](https://github.com/damiandiaz212/oatmeal/actions/workflows/portfolio.yml)
[![Portfolio Web](https://github.com/damiandiaz212/oatmeal/actions/workflows/dashboard.yml/badge.svg)](https://github.com/damiandiaz212/oatmeal/actions/workflows/dashboard.yml)

An advanced lightweight multi-mock portfolio service for traders and developers to train, test, and refine trading algorithms using real stock prices, market sentiments, and various financial indicators. This platform simulates real-world trading environments, offering in-depth analytics to evaluate algorithm performance in risk-free settings.

---
### Features
* Instant algorithm performance analysis
* Multiple unique portfolios 
* Real time order streaming via server events
* Alpha Vantage API ready, just plug in api key
* SQLite persistence

### Run Service (Local)
1. ```cd services```
2. Create a file ALPHA_KEY.txt
3. Paste your api key in that file
4. ```pip install -r requirements.txt```
5. ```python mock_portfolio.py --local```

### Run Dashboard (Local)
1. ```cd dashboard```
2. ```yarn```
3. ```yarn dev```



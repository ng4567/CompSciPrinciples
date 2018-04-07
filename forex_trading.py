author = 'Nikhil Gopal'
from forex_python.converter import  CurrencyRates

c = CurrencyRates() #initialize the exchange rates for every currency

USD_rates = c.get_rates('USD') #USD is the base currency


#list of currencies without USD
list_of_currencies = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'ZAR']



list_of_notable_pairs=[]

for currency in list_of_currencies:

    #initialize a dictionary that contains the exchange rates for a ceratin currency, minus USD
    current_currency_exchange_rates = c.get_rates(currency)

    current_currency_usd_exchange_rate = USD_rates[currency]

    #USD/Current Currency Exchange Rate
    print "USD/" + currency, USD_rates[currency]

    for key in current_currency_exchange_rates: #dictionary of all exchange rates for current currency
        if key == 'USD':
            pass
        else:
            print 'USD/' + key, USD_rates[key],
            print currency + '/' + key, current_currency_exchange_rates[key]
            print "1 USD's worth of " + currency + " buys", USD_rates[currency] * current_currency_exchange_rates[key], key
            print "8888888888"
    break






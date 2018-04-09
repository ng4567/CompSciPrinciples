author = 'Nikhil Gopal'
from forex_python.converter import  CurrencyRates
from heapq import nlargest

c = CurrencyRates() #initialize the exchange rates for every currency

USD_rates = c.get_rates('USD') #USD is the base currency becuase that is what I use as  US resident, can change to suit your own needs


#list of currencies without USD
list_of_currencies = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'ZAR']



dictionary_of_notable_pairs = {} #dictionary that holds how much 1 currencies worth of USD buys of another currency - the USD value
dictionary_of_notable_pairs_absolute_values={}#holds absolute values of the exchange rates, to judge the discrepancies between the currencies
for currency in list_of_currencies:

    #initialize a dictionary that contains the exchange rates for a ceratin currency, minus USD
    current_currency_exchange_rates = c.get_rates(currency)


    #USD/Current Currency Exchange Rate
    #print "USD/" + currency, USD_rates[currency]

    for key in current_currency_exchange_rates: #dictionary of all exchange rates for current currency
        if key == 'USD':
            pass
        else:
            #print 'USD/' + key, USD_rates[key], #print USD/current currency exchange rate
            #print currency + '/' + key, current_currency_exchange_rates[key] #print current currency/currency being iterated exchange rate
            #print "1 USD's worth of " + currency + " buys", USD_rates[currency] * current_currency_exchange_rates[key], key #print what 1USD's worth of X currency buys
            # print "1 USD's worth of " + currency + " buys", converted_value, key
            # print " "

            converted_value = USD_rates[currency] * current_currency_exchange_rates[key]
            dictionary_of_notable_pairs[currency + '/' + key] = converted_value - USD_rates[currency]
            dictionary_of_notable_pairs_absolute_values[currency + '/' + key] = abs(converted_value - USD_rates[currency])


three_best_currency_pairs = nlargest(3,dictionary_of_notable_pairs_absolute_values)
three_best_currency_pairs

print "The three best currency pairs to trade with USD as a starting currency are: " + three_best_currency_pairs[0] + ", " + three_best_currency_pairs[1] + ", " + three_best_currency_pairs[2]


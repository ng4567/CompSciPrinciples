author = 'Nikhil Gopal'
from forex_python.converter import  CurrencyRates
from heapq import nlargest
import pickle

file_handle = "brokerage-names.pk" #initialize a filehandle that accesses a file I use to save list values after the program stops, and whose values I can use anytime

#initialize a variable to tell the computer to select a brokerage or to create a new one
brokerage_or_not = raw_input("welcome, please press type 1 to select a brokerage, q to quit, or anything else to create a new one ")

#dictionary that holds all the information on brokerages format: account balance, maximum leverage as multiplied by acccount balance, commission fee, commmission fee as percent of loss/gain
forex_brokerages_dictionary = {}

#function that allows the user to select their brokerage
def select_brokerage():
    while 4 != 5:

        x = raw_input("press 1 to show the names of the brokerages, press q to quit or press anything else to input a name ")

        if x == "1": #show the names of the brokerages
            with open(file_handle, "rb") as fh: #open the file that contains the list of brokerages
                temp_list = pickle.load(fh) #read the values of the list
            print temp_list
        elif x == "q": #quit the program
            print "the script has stopped"
            exit()
        else: #check to make sure the brokerage exists on file, and selects it if it is, forces user to do it again if not
            brokerage_name = raw_input("input a brokerage name ")
            if brokerage_name in forex_brokerages_dictionary:
                return brokerage_name
            else:
                print "that is not a brokerage on file, the brokerages on file are: " + str(forex_brokerages_dictionary.keys())


if brokerage_or_not == "1": #select a brokerage
    brokerage_name = select_brokerage()
elif brokerage_or_not == 'q': #quit
    print "the script has stopped"
    exit()
else: #user inputs a new brokerage #code in here a mechanism that allows the user to code in a new brokerage see https://stackoverflow.com/questions/31891286/keeping-the-data-of-a-variable-between-runs-of-code

    new_brokerage_name = raw_input("input the name of the new brokerage ")
    new_brokerage_balance = raw_input("input the account balance (no commas) ")
    new_brokerage_max_leverage = raw_input("input the max leverage (no commas) ")
    new_brokerage_commission_fee = raw_input("input the brokerages commission fee per trade, type 0 for 0$ ")
    new_brokerage_commission_fee_as_percent = raw_input("input brokerages commission fee per trade as percentage of loss or gain, type 0 for 0%")
    forex_brokerages_dictionary[new_brokerage_name] = [float(new_brokerage_balance), float(new_brokerage_max_leverage), float(new_brokerage_commission_fee), float(new_brokerage_commission_fee_as_percent)]

    print "New brokerage " + new_brokerage_name + " added."
    print "the script has stopped"
    exit()

#open the pickle file to store any made brokerages
with open(file_handle, 'wb') as fh:
    pickle.dump(forex_brokerages_dictionary, fh)


def calculate_best_forex_trade():

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
        print "USD/" + currency, USD_rates[currency]

        for key in current_currency_exchange_rates: #dictionary of all exchange rates for current currency
            if key == 'USD':
                pass
            else:
                print 'USD/' + key, USD_rates[key], #print USD/current currency exchange rate
                print currency + '/' + key, current_currency_exchange_rates[key] #print current currency/currency being iterated exchange rate
                print "1 USD's worth of " + currency + " buys", USD_rates[currency] * current_currency_exchange_rates[key], key #print what 1USD's worth of X currency buys
                #print "1 USD's worth of " + currency + " buys", converted_value, key
                print " "

                converted_value = USD_rates[currency] * current_currency_exchange_rates[key]
                dictionary_of_notable_pairs[currency + '/' + key] = converted_value - USD_rates[currency]
                dictionary_of_notable_pairs_absolute_values[currency + '/' + key] = abs(converted_value - USD_rates[currency])


    three_best_currency_pairs = nlargest(3,dictionary_of_notable_pairs_absolute_values) #list that contains the three best currency pairs, nlargest function takes the highest values in the list

    print "The three best currency pairs to trade with USD as a starting currency are: " + three_best_currency_pairs[0] + ", " + three_best_currency_pairs[1] + ", " + three_best_currency_pairs[2]

    return three_best_currency_pairs[0] #return the most profitable currency pair


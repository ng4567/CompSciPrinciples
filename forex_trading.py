author = 'Nikhil Gopal'
from forex_python.converter import CurrencyRates
c = CurrencyRates() #initialize the exchange rates for every currency
from heapq import nlargest
import pickle

file_handle = "brokerage-names.pk" #initialize a filehandle that accesses a file I use to save list values after the program stops, and whose values I can use anytime

#initialize a variable to tell the computer to select a brokerage or to create a new one
brokerage_or_not = raw_input("welcome, please press type 1 to select a brokerage, q to quit, or anything else to create a new one ")

#dictionary that holds all the information on brokerages format: account balance, maximum leverage as multiplied by acccount balance, commission fee, commmission fee as percent of loss/gain
forex_brokerages_dictionary = {}

#function that allows the user to select their brokerage, returns the selected
def select_brokerage():

    with open(file_handle, 'rb') as fh: #initiate retrieves saved brokerages from file so that they can be used later
        temp_list = pickle.load(fh)
    forex_brokerages_dictionary = temp_list #saves the brokerages to a list that can be used later


    while 4 != 5:

        x = raw_input("press 1 to show the names of the brokerages, press q to quit or press anything else to input a name ")

        if x == "1": #show the names of the brokerages
            with open(file_handle, "rb") as fh: #open the file that contains the list of brokerages
                temp_list = pickle.load(fh) #read the values of the list to print them
            print 'Brokerages on file (account balance, max leverage, commision fee, commmission as percent of trade: '
            print temp_list
        elif x == "q": #quit the program
            print "the script has stopped"
            exit()
        else: #check to make sure the brokerage exists on file, and selects it if it is, forces user to do it again if not
            brokerage_name = raw_input("input a brokerage name ")

            if brokerage_name in forex_brokerages_dictionary:
                print "brokerage selected: " + brokerage_name
                return brokerage_name
            else:

                print "that is not a brokerage on file, the brokerages on file are: " + str(forex_brokerages_dictionary.keys())


with open(file_handle, 'rb') as fh:
    temporary_dictionary = pickle.load(fh)
forex_brokerages_dictionary = temporary_dictionary


if brokerage_or_not == "1": #select a brokerage, get the brokerage's name in a variable
    brokerage_name = select_brokerage()
elif brokerage_or_not == 'q': #quit program if user wants
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
    brokerage_name = new_brokerage_name





#this function returns the most profitable currency pair, also prints the second and third most profitable
def calculate_best_forex_trade():



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


best_trade = "ZAR/TRY" #calculate_best_forex_trade() uncomment later, don't want to run full function to save time
currency_to_buy_with_dollars = best_trade[0:3]
currency_to_buy_second = best_trade[4:7]



def make_currency_trade(currency1,currency2,brokerage_info):

    #multiply the account balance times the exchange rate of the first currency, we buy this much of the first currency with dollars
    first_exchange_rate = c.get_rate('USD', currency1)
    amount_bought_of_currency_1 = first_exchange_rate * brokerage_info[0] #multiply exchange rate of currency 1 * account balance to get how much currency is bought
    second_exchange_rate = c.get_rate(currency_to_buy_with_dollars,currency2)
    amount_bought_of_second_currency = second_exchange_rate * amount_bought_of_currency_1
    exchange_rate_to_convert_back_to_USD = c.get_rate(currency2, 'USD')
    dollars_at_end_of_trade = exchange_rate_to_convert_back_to_USD * amount_bought_of_second_currency

    profit_made = dollars_at_end_of_trade - brokerage_info[0]
    profit_made -= float(brokerage_info[2])
    profit_made -= profit_made * float(brokerage_info[3])

    potential_profit_using_leverage = profit_made * float(brokerage_info[1])

    return profit_made, potential_profit_using_leverage

x = make_currency_trade(currency_to_buy_with_dollars,currency_to_buy_second,forex_brokerages_dictionary[brokerage_name])


#series of print statements that shows the user what the profit margins look like
print ''
print "potential profit made: " + str(x[0])
print "potential profit made using max amount of leverage: " + str(x[1])
print ''

make_trade_or_not = raw_input('Type y to make this trade or anything else to stop. If you do, your account balance will be updated?')


if make_trade_or_not == "y":
    leverage_or_not = raw_input('Type y to use leverage or anything else to not use leverage')
    if leverage_or_not == "y":
        forex_brokerages_dictionary[brokerage_name][0] += x[1] #update the new account balance with profit made (using leverage)
        print ""
        print "your account balance is: " + str(forex_brokerages_dictionary[brokerage_name][0])
        print ''
        print "the script has stopped"
    else:
        forex_brokerages_dictionary[brokerage_name][0] += x[0] #update the new account balance with the profit made (without leverage)
        print ""
        print "your account balance is: " + str(forex_brokerages_dictionary[brokerage_name][0])
        print ''
        print "the script has stopped"
else:
    print 'the script has stopped'

#open the pickle file and stores newly made brokerages
with open(file_handle, 'wb') as fh:
    pickle.dump(forex_brokerages_dictionary, fh)
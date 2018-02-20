#IMPORTS
import gdax
import json
import websocket
import threading
from pprint import pprint
import time
from statistics import mean
from os import system
from pymongo import MongoClient
import configparser
#import redis

#VARIABLES
    #tickers
magic = {'magic': "wstestETHcomp_v1.31"}
    #tickers
btcusd = {'price':0.0001, 'best_ask':0.0, 'best_bid':0.0}
bchusd = {'price':0.0001, 'best_ask':0.0, 'best_bid':0.0}
ethusd = {'price':0.0001, 'best_ask':0.0, 'best_bid':0.0}
ltcusd = {'price':0.0001, 'best_ask':0.0, 'best_bid':0.0}
ethbtc = {'price':0.0001, 'best_ask':0.0, 'best_bid':0.0}
result = {'product_id':'NA'}
    #balances
btc_bal = "0.0"
bch_bal = "0.0"
eth_bal = "0.0"
ltc_bal = "0.0"
usd_bal = "0.0"

btc_in_usd = "0.0"
bch_in_usd = "0.0"
eth_in_usd = "0.0"
ltc_in_usd = "0.0"

portfolio_value = "0.0"
total_gained = "0.0"
profit_loss = "0.0"
trns_runs = 0
trns_runs_opp = 0
deposited = 7856.65

avrg_arb = 0.001
counter = 0
gain = 0.0
gain_opp = 0.0
inv = 100.0

site = 'wss://ws-feed.gdax.com'
subscribe = {
    "type": "subscribe",
    "product_ids": [
        "BTC-USD",
        "BCH-USD",
        "ETH-USD",
        "LTC-USD",
        "ETH-BTC"
    ],
    "channels": [
        {
            "name": "ticker",
            "product_ids": [
                "BTC-USD",
                "BCH-USD",
                "ETH-USD",
                "LTC-USD",
                "ETH-BTC"
            ]
        }
    ]
}

#FUNCTION DEFENITIONS
def ticker():
    global btcusd
    global bchusd
    global ethusd
    global ltcusd
    global ethbtc

    global trns_runs
    global trns_runs_opp

    global counter
    global avrg_arb
    global gain
    global gain_opp

    global btc_bal
    global bch_bal
    global eth_bal
    global ltc_bal
    ts3 = 0.0

    while True:
        try:
            ts1=time.time()
            result = json.loads(ws.recv())
            system("clear")
            print("        COMBO WSTickerETH BTC->ETH->USD ver 1.31 - 1/25/18")
            if   'BTC-USD' in result['product_id']:
                print('BTC-USD: ' + str(round(float(result['price']),2)), "  Timestamp:", str(result['time']), '\n')
                btcusd = result
            elif 'BCH-USD' in result['product_id']:
                print('BCH-USD: ' + str(round(float(result['price']),2)), "  Timestamp:", str(result['time']), '\n')
                bchusd = result
            elif 'ETH-USD' in result['product_id']:
                print('ETH-USD: ' + str(round(float(result['price']),2)), "  Timestamp:", str(result['time']), '\n')
                ethusd = result
            elif 'LTC-USD' in result['product_id']:
                print('LTC-USD: ' + str(round(float(result['price']),2)), "  Timestamp:", str(result['time']), '\n')
                ltcusd = result
            elif 'ETH-BTC' in result['product_id']:
                print('ETH-BTC: ' + str(round(float(result['price']),7)), "  Timestamp:", str(result['time']), '\n')
                ethbtc = result

            print("   BTC-USD     BCH-USD     ETH-USD     LTC-USD     ETH-BTC  ")
            print(" ", round(float(btcusd['price']),2) , "   ", round(float(bchusd['price']),2) , "     ", round(float(ethusd['price']),2) , "    ", round(float(ltcusd['price']),2) , "    ", round(float(ethbtc['price']),4), "\n")
            print("     BTC         BCH         ETH         LTC         USD")
            print(" ", round(float(btc_bal), 6), "  ", round(float(bch_bal), 6), "      ", round(float(eth_bal),2), "     ", round(float(ltc_bal), 6), "    ", round(float(usd_bal),2))
            btc_in_usd = round(float(str(btcusd['price'])) * float(str(btc_bal)),2)
            bch_in_usd = round(float(str(bchusd['price'])) * float(str(bch_bal)),2)
            eth_in_usd = round(float(str(ethusd['price'])) * float(str(eth_bal)),2)
            ltc_in_usd = round(float(str(ltcusd['price'])) * float(str(ltc_bal)),2)
            portfolio_value = float(usd_bal) + btc_in_usd + bch_in_usd + eth_in_usd + ltc_in_usd
            profit_loss = (float(portfolio_value)/deposited - 1) * 100.0
            total_gained = portfolio_value - deposited
            print("  $", btc_in_usd, "  $", bch_in_usd, "   $", eth_in_usd, "     $", ltc_in_usd)
            print("\nCurrent arbitrage level: %", round(gain/inv*100,4),"    TRANSACTIONS DONE:",trns_runs,)
            print("\nCurrent arbitrage level: %", round(gain_opp/inv*100,4),"    TRANSACTIONS DONE:",trns_runs_opp,'\n')

            print("Deposited: $", deposited)
            print("Portfolio Value: $", round(portfolio_value,2))
            print("Total gained: $", round(total_gained,2))
            print("Profit: %", round(profit_loss,2))

            counter+=1
            ts2 = time.time()-ts1
            ts3 += ts2
            # averageRunTime.append(ts2)
            print("\nRun #", counter, "time:", round(ts2,2), "average:", round(ts3/counter,2), "time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            #print("   ", round(float(btc_in_usd),2), "   ", round(float(bch_in_usd),2), "   ", round(float(eth_in_usd),2), "   ", usd)
            #pprint(result)


        except BaseException as err:
            print(err)
            pass

def get_account_data():
    #GLOBAL VARIABLES
    global btc_acc_id
    global bch_acc_id
    global eth_acc_id
    global ltc_acc_id
    global usd_acc_id

    global btc_acc
    global bch_acc
    global eth_acc
    global ltc_acc
    global usd_acc

    global btc_bal
    global bch_bal
    global eth_bal
    global ltc_bal
    global usd_bal

    global btc_in_usd
    global bch_in_usd
    global eth_in_usd
    global ltc_in_usd

    global btcusd
    global bchusd
    global ethusd
    global ltcusd

    global counter
    while True:

        try:    #GET ACCOUNT INFO
            btc_acc = auth_client.get_account(btc_acc_id)
            bch_acc = auth_client.get_account(bch_acc_id)
            eth_acc = auth_client.get_account(eth_acc_id)
            usd_acc = auth_client.get_account(usd_acc_id)
            ltc_acc = auth_client.get_account(ltc_acc_id)

            btc_bal = btc_acc['balance']
            bch_bal = bch_acc['balance']
            eth_bal = eth_acc['balance']
            usd_bal = usd_acc['balance']
            ltc_bal = ltc_acc['balance']
        except BaseException as err:
            print("ACCOUNT THREAD ERROR:", err)
            pass

    #CURRENCY VALUE CALCULATE IN USD

def arbitrage(inv):
    global btcusd
    global ethusd
    global ethbtc
    global gain
    global avrg_arb
    counter = 1
    print("*"*50)
    time.sleep(5)
    print("*"*50,inv)
    while True:
        try:
            btc = inv / float(str(btcusd['best_ask']))
            eth = btc / float(str(ethbtc['best_ask']))
            usd = eth * float((ethusd['best_bid']))

            gain = usd - inv
            if gain/inv >= 0.0085:
                transact(inv)
                print('\a'*1)
                # time.sleep(1)
        except BaseException as err:
            print("ARBITRAGE THREAD ERROR:", err)
            pass

def arbitrage_opp(inv):
    global btcusd
    global ethusd
    global ethbtc
    global gain_opp
    global avrg_arb
    counter = 1
    print("*"*50)
    time.sleep(5)
    print("*"*50,inv)
    while True:
        try:
            eth = inv / float(str(ethusd['best_ask']))
            btc = eth * float(str(ethbtc['best_bid']))
            usd = btc * float((btcusd['best_bid']))

            gain_opp = usd - inv
            if gain_opp/inv >= 0.0085:
                transact_opp(inv)
                print('\a'*1)
                # time.sleep(1)
        except BaseException as err:
            print("ARBITRAGE_OPP THREAD ERROR:", err)
            pass

def transact(amount):
    global btcusd
    global ethusd
    global ethbtc
    global trns_runs
    #     Trans 1 USD -> BTC
    try:
        btc_lot = round(amount / float(btcusd['best_ask']),8)
        # Buy 0.01 BTC @ 100 USD
        response_btcusd = auth_client.buy(price=btcusd['best_ask'], #USD
                   size=str(btc_lot), #BTC
                   product_id='BTC-USD')
        #     Trans 2 BTC -> LTC
        pprint(response_btcusd)
        eth_lot = round(btc_lot / float(ethbtc['best_ask']),7)
        # Buy 0.01 LTC @ 100 BTC
        response_ethbtc = auth_client.buy(price=ethbtc['best_ask'], #USD
                   size=str(eth_lot), #BTC
                   product_id='ETH-BTC')
        pprint(response_ethbtc)
        #     Trans 3 LTC -> USD
        # Sell 0.01 LTC @ 200 USD
        response_ethusd = auth_client.sell(price=ethusd['best_bid'], #USD
                   size=str(eth_lot), #BTC
                   product_id='ETH-USD')
        pprint(response_ethusd)
        details = {"Arb_lvl":gain/inv*100, 'batch_id':int(time.strftime("%Y%m%d"))*1000000+counter,'direction':'reg','trns_role':'entry'}
        magic.update(details)
        response_btcusd.update(magic)
        magic.update({'trns_role':'conv'})
        response_ethbtc.update(magic)
        magic.update({'trns_role':'exit'})
        response_ethusd.update(magic)
        collection.insert(response_btcusd)
        collection.insert(response_ethbtc)
        collection.insert(response_ethusd)
        trns_runs += 1
    except BaseException as err:
        print ("TRANSACT FUNCTION ERROR:", err)
        pass

def transact_opp(amount):
    global btcusd
    global ethusd
    global ethbtc
    global trns_runs_opp
    #     Trans 1 USD -> BTC
    try:
        eth_lot = round(amount / float(ethusd['best_ask']),8)
        # Buy 0.01 BTC @ 100 USD
        response_ethusd = auth_client.buy(price=ethusd['best_ask'], #USD
                   size=str(eth_lot), #BTC
                   product_id='ETH-USD')
        #     Trans 2 BTC -> LTC
        pprint(response_ethusd)
        btc_lot = round(eth_lot * float(ethbtc['best_bid']),7)
        # Buy 0.01 LTC @ 100 BTC
        response_ethbtc = auth_client.sell(price=ethbtc['best_bid'], #USD
                   size=str(eth_lot), #BTC
                   product_id='ETH-BTC')
        pprint(response_ethbtc)
        #     Trans 3 LTC -> USD
        # Sell 0.01 LTC @ 200 USD
        response_btcusd = auth_client.sell(price=btcusd['best_bid'], #USD
                   size=str(btc_lot), #BTC
                   product_id='BTC-USD')
        pprint(response_btcusd)
        #r.execute_command('JSON.SET', 'tr1', '.', json.dumps(response_ethusd))
        #r.execute_command('JSON.SET', 'tr2', '.', json.dumps(response_ethbtc))
        #r.execute_command('JSON.SET', 'tr3', '.', json.dumps(response_btcusd))
        details = {"Arb_lvl":gain_opp/inv*100, 'batch_id':int(time.strftime("%Y%m%d"))*1000000+counter, 'direction':'opp','trns_role':'entry'}
        magic.update(details)
        response_ethusd.update(magic)
        magic.update({'trns_role':'conv'})
        response_ethbtc.update(magic)
        magic.update({'trns_role':'exit'})
        response_btcusd.update(magic)
        collection.insert(response_ethusd)
        collection.insert(response_ethbtc)
        collection.insert(response_btcusd)
        trns_runs_opp += 1
    except BaseException as err:
        print ("TRANSACT OPP FUNCTION ERROR:", err)
        pass

#API SETUP
config = configparser.ConfigParser()
config.read('config.ini')

    #authenticate user
api_key = config['API']['api_key']
api_secret = config['API']['api_secret']
passphrase = config['API']['passphrase']
auth_client = gdax.AuthenticatedClient(api_key, api_secret, passphrase)
public_client = gdax.PublicClient()

    #set accounts IDs
btc_acc_id = config['ACCOUNT_IDS']['btc_acc_id']
bch_acc_id = config['ACCOUNT_IDS']['bch_acc_id']
eth_acc_id = config['ACCOUNT_IDS']['eth_acc_id']
usd_acc_id = config['ACCOUNT_IDS']['usd_acc_id']
ltc_acc_id = config['ACCOUNT_IDS']['ltc_acc_id']

    #init acc variables
btc_acc = auth_client.get_account(btc_acc_id)
bch_acc = auth_client.get_account(bch_acc_id)
eth_acc = auth_client.get_account(eth_acc_id)
usd_acc = auth_client.get_account(usd_acc_id)
ltc_acc = auth_client.get_account(ltc_acc_id)

#WEBSOCKET SETUP
ws = websocket.create_connection(site)
ws.send(json.dumps(subscribe))

#REDIS SETUP
#r = redis.Redis()

#MONGODB SETUP
connection_data = config['MONGODB']['string']
mongo_client = MongoClient(connection_data)
db = mongo_client.cryptocurrency_database
collection = db.transaction_test

tempqt = public_client.get_product_ticker(product_id='BTC-USD')
btcusd['price'] = tempqt['price']
btcusd['best_ask'] = tempqt['ask']
btcusd['best_bid'] = tempqt['bid']
tempqt = public_client.get_product_ticker(product_id='ETH-USD')
ethusd['price'] = tempqt['price']
ethusd['best_ask'] = tempqt['ask']
ethusd['best_bid'] = tempqt['bid']
tempqt = public_client.get_product_ticker(product_id='ETH-BTC')
ethbtc['price'] = tempqt['price']
ethbtc['best_ask'] = tempqt['ask']
ethbtc['best_bid'] = tempqt['bid']

#TICKER THREAD INIT
thrd_ticker = threading.Thread(target = ticker,)
thrd_account_data = threading.Thread(target = get_account_data,)
thrd_arbitrage = threading.Thread(target = arbitrage, args=[inv,])
thrd_arbitrage_opp = threading.Thread(target = arbitrage_opp, args=[inv,])
thrd_account_data.start()
thrd_ticker.start()
thrd_arbitrage.start()
thrd_arbitrage_opp.start()

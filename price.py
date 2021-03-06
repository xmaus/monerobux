#romerito -*- coding: UTF-8 -*-
import sopel.module
import requests
import time
import random
import datetime
# from apikey import commodity_key

polourl = "https://poloniex.com/public?command=returnTicker"
poloxmrlendurl = "https://poloniex.com/public?command=returnLoanOrders&currency=XMR&limit=999999"
polobtclendurl = "https://poloniex.com/public?command=returnLoanOrders&currency=BTC&limit=999999"
prevamnt, prevtime = 0, 0
trexurl = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-"
cryptopiaurl = "https://www.cryptopia.co.nz/api/GetMarkets"
bitsquareurl = "https://market.bitsquare.io/api/ticker/?market=xmr_btc"
finexbtc = 'https://api.bitfinex.com/v1/pubticker/XMRBTC'
finexusd = 'https://api.bitfinex.com/v1/pubticker/XMRUSD'
krakbtc = 'https://api.kraken.com/0/public/Ticker?pair=XMRXBT'
krakbtceur = 'https://api.kraken.com/0/public/Ticker?pair=XBTEUR'
krakusd = 'https://api.kraken.com/0/public/Ticker?pair=XMRUSD'
krakeur = 'https://api.kraken.com/0/public/Ticker?pair=XMREUR'
kraktrig = 'https://api.kraken.com/0/public/Ticker?pair='  #append coin/trigger in function below
okcquar = 'https://www.okcoin.com/api/v1/future_ticker.do?symbol=btc_usd&contract_type=quarter'
krakusdt = 'http://api.kraken.com/0/public/Ticker?pair=USDTUSD'
bitflyerurl = 'https://api.bitflyer.jp/v1/ticker'
thumbxmrurl = 'https://api.bithumb.com/public/ticker/xmr'	# measured natively in KRW
thumbbtcurl = 'https://api.bithumb.com/public/ticker/btc'	# measured natively in KRW
binanceurl = 'https://api.binance.com/api/v1/ticker/24hr'
localmonerousd = 'https://localmonero.co/api/ticker?currencyCode=USD'
ogreurl = 'https://tradeogre.com/api/v1/markets'

@sopel.module.commands('forksum')
def forksum(bot, trigger):
    url = 'https://api.coinmarketcap.com/v1/ticker/?bch'
    try:
        r = requests.get(url)
        j = r.json()
        for i in j:
            try:
                if i['id'] == 'bitcoin':
                    btcprice = float(i['price_usd'])
                if i['id'] == 'bitcoin-cash':
                    bcashprice = float(i['price_usd'])
                if i['id'] == 'bitcoin-gold':
                    bgoldprice = float(i['price_usd'])
            except: pass
        bot.say("The sum of USD price of BTC, BCH, and BTG is ${:.2f}".format(btcprice+bcashprice+bgoldprice))
    except:
        bot.say("Error parsing ticker")

@sopel.module.commands('ath')
def ath(bot, trigger):
    with open('/root/.sopel/modules/ath.log', 'r') as f:
        text = f.read()
    btcath = float(text.split(' ')[0])
    btcathdate = text.split(' ')[1]
    usdath = float(text.split(' ')[2])
    usdathdate = text.split(' ')[3]
    update = False
    url = 'https://api.coinmarketcap.com/v1/ticker/monero'
    r = requests.get(url)
    j = r.json()
    price_btc = float(j[0]['price_btc'])
    price_usd = float(j[0]['price_usd'])
    if price_btc > btcath:
        btcath = price_btc
        update = True
        btcathdate = datetime.datetime.fromtimestamp(int(coin['last_updated'])).strftime('%Y-%m-%d')
    if price_usd > usdath:
        usdath = price_usd
        update = True
        usdathdate = datetime.datetime.fromtimestamp(int(coin['last_updated'])).strftime('%Y-%m-%d')
    if update == True:
        with open('/root/.sopel/modules/ath.log', 'w') as f:
            f.write("{} {} {} {}".format(btcath, btcathdate, usdath, usdathdate))
    bot.say("BTC ath = {} on {}. USD ath = ${} on {}".format(btcath, btcathdate, usdath, usdathdate))

@sopel.module.commands('bfx', 'bitfinex')
def bfx(bot, trigger):
    stringtosay = ''
    try:
        r = requests.get(finexbtc)
        j = r.json()
        stringtosay += "Last XMR/BTC trade at {0:.6f} on {1:.2f} 24 h XMR volume. ".format(float(j['last_price']), float(j['volume']))
    except:
        bot.say("Error getting XMR/BTC data")
    try:
        r = requests.get(finexusd)
        j = r.json()
        stringtosay += "Last XMR/USD trade at {0:.2f} on {1:.2f} 24 h XMR volume.".format(float(j['last_price']), float(j['volume']))
    except:
        bot.say("Error getting XMR/USD data")
    try:
        bot.say(stringtosay)
    except:
        bot.say("Error getting data")

@sopel.module.commands('krak', 'kraken')
def krak(bot, trigger):
    stringtosay = ''
    if not trigger.group(2):
        try:
            r = requests.get(krakbtc)
            j = r.json()
            stringtosay += "Last XMR/BTC trade at {0:.6f} on {1:.2f} 24 h XMR volume. ".format(float(j['result']['XXMRXXBT']['c'][0]), float(j['result']['XXMRXXBT']['v'][1]))
        except:
            bot.say("Error getting XMR/BTC data")
        try:
            r = requests.get(krakusd)
            j = r.json()
            stringtosay += "Last XMR/USD trade at {0:.2f} on {1:.2f} 24 h XMR volume. ".format(float(j['result']['XXMRZUSD']['c'][0]), float(j['result']['XXMRZUSD']['v'][1]))
        except:
            bot.say("Error getting XMR/USD data")
        try:
            r = requests.get('https://api.kraken.com/0/public/Ticker?pair=XMREUR')  #shouldn't this be krakeur?
            j = r.json()
            stringtosay += "Last XMR/EUR trade at {0:.2f} on {1:.2f} 24 h XMR volume. ".format(float(j['result']['XXMRZEUR']['c'][0]), float(j['result']['XXMRZEUR']['v'][1]))
        except:
            bot.say("Error getting XMR/EUR data")
        try:
            bot.say(stringtosay)
        except:
            bot.say("Error getting data")
    else:
        coin = trigger.group(2).upper()
        try:
            r=requests.get(kraktrig+coin+'XBT')
            j=r.json()
	    stringtosay += "{0} at {1:.8f} on {2:.2f} 24 h {0} volume. ".format(coin, float(j['result']['X'+str(coin)+'XXBT']['c'][0]), float(j['result']['X'+str(coin)+'XXBT']['v'][1]))
	except:
            bot.say("Error connecting to Kraken")
	try:
            bot.say(stringtosay)
        except:
            bot.say("Error getting data")

@sopel.module.commands('usdt')
def usdt(bot, trigger):
    try:
        r = requests.get(krakusdt)
        j = r.json()
        stringtosay = "Last USDT/USD trade at ${0:.4f} on {1:.2f} USD 24 h volume. Highest bid at ${2:.4f}".format(float(j['result']['USDTZUSD']['c'][0]), float(j['result']['USDTZUSD']['v'][0]), float(j['result']['USDTZUSD']['b'][0]))
        bot.say(stringtosay)
    except:
        bot.say("Error getting USDT/USD data")

@sopel.module.commands('btckrak', 'btckraken', 'btceur')
def krakeur(bot, trigger):
    stringtosay = ''
    try:
        r = requests.get(krakbtceur)
        j = r.json()
        stringtosay += "Last BTC/EUR trade at €{0:.2f} on {1:.2f} BTC 24 h volume. ".format(float(j['result']['XXBTZEUR']['c'][0]), float(j['result']['XXBTZEUR']['v'][0]))
    except:
        bot.say("Error getting BTC/EUR data")
    try:
        bot.say(stringtosay)
    except:
        bot.say("Error getting data")

@sopel.module.commands('chart')
def chart(bot, trigger):
    bot.say('https://cryptowat.ch/poloniex/xmrbtc')

@sopel.module.commands('polo', 'poloniex', 'marco')
@sopel.module.interval(3600)
def polo(bot, trigger):
    if not trigger.group(2):
        try:
            r=requests.get(polourl)
            j=r.json()
            xmr=j["BTC_XMR"]
            last=float(xmr['last'])
            change=float(xmr['percentChange'])
            vol=float(xmr['baseVolume'])
            if change >= 0:
                sign = '+'
            else:
                sign = ''
            face = ''
            if change > 0.10:
                face = u'\u263d'.encode('utf8')
            if 0.10 >= change > 0.05:
                face = u'\u2661'.encode('utf8')
            if 0.05 >= change > 0.02:
                face = u'\u263a'.encode('utf8')
            if 0.02 >= change > -0.02:
                face = u'\u2694'.encode('utf8')
            if -0.02 >= change > -0.05:
                face = u'\u2639'.encode('utf8')
            if -0.05 >= change > -0.1:
                face = u'\u2620'.encode('utf8')
            if change < -0.1:
                face = u'\u262d'.encode('utf8')
            bot.say("Poloniex at {0:.8f} BTC; {1}{2:.2f}% over 24 hours on {3:.3f} BTC volume {4}".format(last, sign, change*100, vol, face))
        except:
            bot.say("Error retrieving data from Poloniex")
    else:
        coin = trigger.group(2).upper()
        try:
            r=requests.get(polourl)
            j=r.json()
        except:
            bot.say("Error connecting to Poloniex")
        if len(coin) > 5 or len(coin) < 2:
            bot.say("Coin ticker is too long or short")
        # elif coin == "PASC":
        #     bot.say("COBOL only in #monero-markets")
        # elif coin == "NAUT":
        #     bot.say("That ship has sailed...")
        elif coin == "PIVX":
            bot.say("Masternodes + PoS...what could possibly go wrong?")
        else:
            label="BTC_" + coin
            try:
                ticker=j[label]
                last=float(ticker['last'])
                change=float(ticker['percentChange'])
                vol=float(ticker['baseVolume'])
                if change >= 0:
                    sign = '+'
                else:
                    sign = ''
                bot.say("{0} at {1:.8f} BTC; {2}{3:.2f}% over 24 hours on {4:.3f} BTC volume".format(coin, last, sign, change*100, vol))
            except:
                bot.say("ERROR!")

@sopel.module.commands('lending')
def lending(bot, trigger):
    try:
        r=requests.get(poloxmrlendurl)
        j=r.json()
        amnt=0
        currenttime=time.time()
        for i in j['offers']:
            amnt+=float(i['amount'])
        bot.say("Total amount of XMR available {0:,.2f}. Changed by {1:.2f} in the last {2:.2f} hours".format(amnt, amnt-prevamnt, (currenttime-prevtime)/3600))
        global prevamnt
        prevamnt=amnt
        global prevtime
        prevtime=currenttime
    except:
        bot.say("Something bad happened :o")

@sopel.module.commands('btclending')
def btclending(bot, trigger):
    try:
        r=requests.get(polobtclendurl)
        j=r.json()
        amnt=0
        amnt10=0
        rate10=0
        amnt100=0
        rate100=0
        for i in j['offers']:
            if amnt < 10:
                amnt10=amnt
                rate10=float(i['rate'])
            if amnt < 100:
                amnt100=amnt
                rate100=float(i['rate'])
            amnt+=float(i['amount'])
        bot.say("Minimum rate is {0:.3f}%. To borrow {1:,.2f} BTC need up to rate {2:.3f}%. To borrow {3:,.2f} BTC need up to rate {4:.3f}%. Total amount is {5:,.2f} BTC at max rate {6:.3f}%".format(float(j['offers'][0]['rate'])*100, amnt10, rate10*100, amnt100, rate100*100, amnt, float(j['offers'][-1]['rate'])*100))
    except:
        bot.say("Something bad happened :o")


@sopel.module.commands('trex', 'bittrex')
def trex(bot, trigger):
    if not trigger.group(2):
         geturl = trexurl+'xmr'
    else:
        geturl = trexurl + trigger.group(2)
    try:
        r = requests.get(geturl)
        j = r.json()
        xmr=j['result'][0]
        last=float(xmr['Last'])
        change=((last/float(xmr['PrevDay']))-1)
        vol=float(xmr['BaseVolume'])
        bot.say("Bittrex at {0:.8f} BTC; {1:.2f}% over 24 hours on {2:.3f} BTC volume".format(last, change*100, vol))
    except:
        bot.say("Error retrieving data from Bittrex")

@sopel.module.commands('tradeogre', 'ogre')
def ogre(bot, trigger):
    if not trigger.group(2):
        pair = 'BTC-XMR'
    else:
        pair = 'BTC-'+trigger.group(2).upper()
    try:
        r = requests.get(ogreurl)
        j = r.json()
        for i in j:
            if pair == i.keys()[0]:
                last=float(i[pair]['price'])
                vol=float(i[pair]['volume'])
        bot.say("{0} on Tradeogre at {1:.8f} BTC on {2:.3f} BTC volume".format(pair, last, vol))
    except:
        bot.say("Error retrieving data from Ogre")

@sopel.module.commands('bsq', 'bitsquare')
def bsq(bot, trigger):
    try:
        r = requests.get(bitsquareurl)
        j = r.json()
        xmr=j['xmr_btc']
        last=float(xmr['last'])
        vol=float(xmr['volume_right'])
        bot.say("Bitsquare at {0:.8f} BTC on {1:.3f} BTC volume".format(last, vol))
    except:
        bot.say("Error retrieving data from Bitsquare")

@sopel.module.commands('binance')
def binance(bot, trigger):
    try:
        if not trigger.group(2):
             coin = 'XMR'
             pair = 'BTC'
        else:
            coin = trigger.group(2).split(' ')[0].upper()
            try:
                if len(trigger.group(2).split(' ')[1]) > 1:
                    pair = trigger.group(2).split(' ')[1].upper()
                else:
                    pair = "BTC"
            except:
                pair = "BTC"
        r = requests.get(binanceurl)
        j = r.json()
        found = False
        for i in j:
            if i["symbol"] == coin+pair:
                last=float(i['lastPrice'])
                change=float(i['priceChangePercent'])
                vol=float(i['volume'])
                bot.say("{0} on Binance at {1:.8f} {2}; {3:.2f}% over 24 hours on {4:.3f} {2} volume".format(coin, last, pair, change, vol*last))
                found = True
        if found == False:
            bot.say("Too scammy even for Binance")
    except:
        bot.say("Error retrieving data from Binance")

@sopel.module.commands('cryptopia', 'shitopia', 'topia', 'ctop')
def cryptopia(bot, trigger):
    try:
        if not trigger.group(2):
             coin = 'XMR'
             pair = 'BTC'
        else:
            coin = trigger.group(2).split(' ')[0].upper()
            try:
                if len(trigger.group(2).split(' ')[1]) > 1:
                    pair = trigger.group(2).split(' ')[1].upper()
                else:
                    pair = "BTC"
            except:
                pair = "BTC"
        r = requests.get(cryptopiaurl)
        j = r.json()
        found = False
        for i in j["Data"]:
            if i["Label"] == coin+"/"+pair:
                last=float(i['LastPrice'])
                change=float(i['Change'])
                vol=float(i['Volume'])
                bot.say("{0} on Cryptopia at {1:.8f} {2}; {3:.2f}% over 24 hours on {4:.3f} {2} volume".format(coin, last, pair, change, vol*last))
                found = True
        if found == False:
            bot.say("This shit is too shitty even for shitopia")
    except:
        bot.say("Error retrieving data from Cryptopia")

@sopel.module.commands('cmc', 'coinmarketcap')
def cmc(bot, trigger):
    # try:
    #     if trigger.group(2).lower() == 'trx':
    #         bot.say("Fuck off with your scams scammer")
    #         return
    # except:
    #     pass
    try:
        r = requests.get('https://api.coinmarketcap.com/v1/ticker?limit=1500')
        j = r.json()
    except:
        bot.say("Can't connect to API")
    if not trigger.group(2):
        c1 = 'XMR'
    else:
        if ' ' in trigger.group(2):
            c1 = trigger.group(2).split(' ')[0].upper()
            c2 = trigger.group(2).split(' ')[1].upper()
        else:
            if trigger.group(2).isdigit():
                rank = trigger.group(2)
            elif trigger.group(2) == 'random':
                rank = random.randint(1,1500)
            else:
                c1 = trigger.group(2).upper()
    try:
        if not 'c2' in locals():
            for i in j:
                try:
                    if i['symbol'] == c1:
                        coin = i
                except: pass
                try:
                    if i['rank'] == str(rank):
                        coin = i
                except: pass
            symbol = coin['symbol']
            name = coin['name']
            rank = coin['rank']
            price_usd = float(coin['price_usd'])
            price_btc = float(coin['price_btc'])
            volume_usd = float(coin['24h_volume_usd'])
            market_cap_usd = float(coin['market_cap_usd'])
            available_supply = float(coin['available_supply'])
            total_supply = float(coin['total_supply'])
            percent_change_24h = float(coin['percent_change_24h'])
            bot.say("{0} ({1}) is #{2}. Last price ${3:.2f} / ฿{4:.8f}. 24h volume ${5:,.0f} changed {6}%. Market cap ${7:,.0f}. Available / total coin supply {8:,.0f} / {9:,.0f}.".format(name, symbol, rank, price_usd, price_btc, volume_usd, percent_change_24h, market_cap_usd, available_supply, total_supply))
        else:
            for i in j:
                try:
                    if i['symbol'] == c1:
                        coin = i
                    if i['symbol'] == c2:
                        c2coin = i
                except: pass
            symbol = coin['symbol']
            c2symbol = c2coin['symbol']
            name = coin['name']
            rank = coin['rank']
            price_usd = float(coin['price_usd'])
            price_btc = float(coin['price_btc'])
            c2price_btc = float(c2coin['price_btc'])
            volume_usd = float(coin['24h_volume_usd'])
            market_cap_usd = float(coin['market_cap_usd'])
            available_supply = float(coin['available_supply'])
            total_supply = float(coin['total_supply'])
            percent_change_24h = float(coin['percent_change_24h'])
            bot.say("{0} ({1}) is #{2}. Last price ${3:.2f} / {4:.8f} {1}/{5}. 24h volume ${6:,.0f}. Market cap ${7:,.0f}. Available / total coin supply {8:,.0f} / {9:,.0f}.".format(name, symbol, rank, price_usd, price_btc/c2price_btc, c2symbol, volume_usd, market_cap_usd, available_supply, total_supply))
    except:
        bot.say("Error parsing ticker")
    try:
        if c1 == 'XMR':
            with open('/root/.sopel/modules/ath.log', 'r') as f:
                text = f.read()
            btcath = float(text.split(' ')[0])
            btcathdate = text.split(' ')[1]
            usdath = float(text.split(' ')[2])
            usdathdate = text.split(' ')[3]
            update = False
            if price_btc > btcath:
                btcath = price_btc
                update = True
                btcathdate = datetime.datetime.fromtimestamp(int(coin['last_updated'])).strftime('%Y-%m-%d')
            if price_usd > usdath:
                usdath = price_usd
                update = True
                usdathdate = datetime.datetime.fromtimestamp(int(coin['last_updated'])).strftime('%Y-%m-%d')
            if update == True:
                with open('/root/.sopel/modules/ath.log', 'w') as f:
                    f.write("{} {} {} {}".format(btcath, btcathdate, usdath, usdathdate))
    except:
        pass

@sopel.module.commands('top')
def top(bot, trigger):
    topXstring = ""
    try:
        try:
        	r = requests.get('https://api.coinmarketcap.com/v1/global/')
        	j = r.json()
        	usd_total_mkt_cap = float(j['total_market_cap_usd'])
        	total_mcap_short = int(int(round(usd_total_mkt_cap,-9))/int(1e9))
        	rounded_total_mcap = str(total_mcap_short)+"B"
        	topXstring += "Total market cap $" + rounded_total_mcap + " | "
        except:
        	bot.say("Can't connect to coinmarketcap API")
        if not trigger.group(2):
            limit = 20
        else:
            limit = int(trigger.group(2))
            if limit > 20:
                bot.say("Too high!  Max is 20!")
            elif limit < 1:
                bot.say("Dude...")
    	r = requests.get('https://api.coinmarketcap.com/v1/ticker?limit={}'.format(limit))
    	j = r.json()
        for i in j:
            symbol = i['symbol']
            name = i['name']
            rank = i['rank']
            price_usd = float(i['price_usd'])
            price_btc = float(i['price_btc'])
            market_cap_usd = float(i['market_cap_usd'])
            if market_cap_usd >= 1e9:
    	        if market_cap_usd >= 1e10:
                    market_cap_short = int(int(round(market_cap_usd,-9))/int(1e9))
    	        else:
    	            market_cap_short = float(round(market_cap_usd,-8)/1e9)
               	rounded_mcap = str(market_cap_short)+"B"
            else:
            	rounded_mcap = "tiny"
            topXstring += "{0}. {1} ${2} | ".format(rank, symbol, rounded_mcap) #TODO: add price_usd, rounded
        bot.say(topXstring[:-2])
    except:
        bot.say("The use is 'top' and then a digit 1 - 20")

@sopel.module.commands('okc', 'okcoin')
def okc(bot, trigger):
    try:
        r = requests.get(okcquar)
        j = r.json()
        xmr=j['ticker']
        last=float(xmr['last'])
        vol=float(xmr['vol'])
        bot.say("OKcoin quarterly futures at ${0:.2f} on {1:.0f} volume".format(last, vol))
    except:
        bot.say("Error retrieving data from OKCoin")

@sopel.module.commands('tux')
def tux(bot, trigger):
    try:
        r = requests.get('https://tuxexchange.com/api?method=getticker')
        j = r.json()
        if not trigger.group(2):
            ticker='XMR'
        else:
            ticker=trigger.group(2).upper()
        coin=j['BTC_{}'.format(ticker)]
        last=float(coin['last'])
        vol=float(coin['baseVolume'])
        change=float(coin['percentChange'])
        bot.say("{0} at {1:.8f} BTC on {2:.3f} BTC volume, changed {3:.2f}% over last 24 hr".format(ticker, last, vol, change))
    except:
        bot.say("Error retrieving data from Tuxexchange")

@sopel.module.commands('pepe', 'pepecash')
def pepe(bot, trigger):
    try:
        r = requests.get('https://tuxexchange.com/api?method=getticker')
        j = r.json()
        pepe=j['BTC_PEPECASH']
        last=float(pepe['last'])
        vol=float(pepe['baseVolume'])
        change=float(pepe['percentChange'])
        bot.say("Pepecash at {0:.8f} BTC on {1:.3f} BTC volume, changed {2:.2f}% over last 24 hr".format(last, vol, change))
    except:
        bot.say("Error retrieving data from Tuxexchange")

@sopel.module.commands('pepexmr')
def pepexmr(bot, trigger):
    try:
        r = requests.get('https://tuxexchange.com/api?method=getticker')
        j = r.json()
        pepe=j['BTC_PEPECASH']
        pepelast=float(pepe['last'])
        r=requests.get(polourl)
        j=r.json()
        xmr=j["BTC_XMR"]
        xmrlast=float(xmr['last'])
        bot.say("Pepe/XMR ratio is : {0:.8f}".format(pepelast/xmrlast))
    except:
        bot.say("FAILURE!")


@sopel.module.commands('tall')
def tall(bot, trigger):
    stringtosend = ''
    stampurl = 'https://www.bitstamp.net/api/ticker/'
    finexurl = 'https://api.bitfinex.com/v1/pubticker/BTCUSD'
    btccurl  = 'https://data.btcchina.com/data/ticker?market=btccny'
    gemiurl  = 'https://api.gemini.com/v1/pubticker/btcusd'
    gdaxurl  = 'https://api.gdax.com/products/BTC-USD/ticker'
    # Bitstamp
    try:
        stampresult = requests.get(stampurl)
        stampjson = stampresult.json()
    except:
	stampjson = False
    if stampjson:
        stringtosend += "Bitstamp last: ${0:,.2f}, vol: {1:,.1f} | ".format(float(stampjson['last']), float(stampjson['volume']))
    # Gemini
    try:
        gemiresult = requests.get(gemiurl)
        gemijson = gemiresult.json()
    except:
	gemijson = False
    if gemijson:
        try:
            stringtosend += "Gemini last: ${0:,.2f}, vol: {1:,.1f} | ".format(float(gemijson['last']), float(gemijson['volume']['BTC']))
        except:
            pass
    # Gdax
    try:
        gdaxresult = requests.get(gdaxurl)
        gdaxjson = gdaxresult.json()
        gdaxprice = float(gdaxjson['price'])
        gdaxvolume = float(gdaxjson['volume'])
    except:
	gdaxjson = False
    if gdaxjson:
        stringtosend += "CBP last: ${0:,.2f}, vol: {1:,.1f} | ".format(gdaxprice, gdaxvolume)
    # Binance
    try:
        binanceresult = requests.get(binanceurl)
        binancejson = binanceresult.json()
        for i in binancejson:
            if i["symbol"] == "BTCUSDT":
                binanceprice = float(i['lastPrice'])
                binancevolume = float(i['volume'])
    except:
	binancejson = False
    if binancejson:
        stringtosend += "Binance last: ${0:,.2f}, vol: {1:,.1f} | ".format(binanceprice, binancevolume)
    # Bitfinex
    try:
        finexresult = requests.get(finexurl)
        finexjson = finexresult.json()
    except:
	finexjson = False
    try:
        if finexjson:
            stringtosend += "Bitfinex last: ${0:,.2f}, vol: {1:,.1f} | ".format(float(finexjson['last_price']), float(finexjson['volume']))
    except:
        stringtosend += "Finex sucks | "
    # Bitthumb
    try:
        thumbresult = requests.get(thumbbtcurl)
        thumbjson = thumbresult.json()
        if thumbjson['data']:
            pass
    except:
	thumbjson = False
    if thumbjson:
        stringtosend += "Bithumb last: ₩{0:,.2f}, vol: {1:,.1f} | ".format(float(thumbjson['data']['buy_price']), float(thumbjson['data']['volume_1day']))
    # Bitflyer
    try:
        bitflyerresult = requests.get(bitflyerurl)
        bitflyerjson = bitflyerresult.json()
    except:
	bitflyerjson = False
    if bitflyerjson:
        stringtosend += "Bitflyer last: ¥{0:,.2f}, vol: {1:,.1f} | ".format(float(bitflyerjson['ltp']), float(bitflyerjson['volume_by_product']))
    # Send the tickers to IRC
    bot.say(stringtosend[:-2])


@sopel.module.commands('xmrtall', 'xmr')
def xmrtall(bot, trigger):
    stringtosend = ''

    # Bithumb (Note: Must calculate BTCXMR price from BTCKRW and XMRKRW)
    try:
	xmr_r = requests.get(thumbxmrurl)
	btc_r = requests.get(thumbbtcurl)
	xmrjson = xmr_r.json()
	btcjson = btc_r.json()
	# No last price in api.  Must average buy and sell price.
	thumbXMRbuy = float(xmrjson['data']['buy_price'])
	thumbXMRsell = float(xmrjson['data']['sell_price'])
	thumbXMRkrw = (thumbXMRbuy + thumbXMRsell)/2
	# Same for BTC
	thumbBTCbuy = float(btcjson['data']['buy_price'])
	thumbBTCsell = float(btcjson['data']['sell_price'])
	thumbBTCkrw = (thumbBTCbuy + thumbBTCsell)/2
	# Finally, price in BTC, and volume in XMR
	thumbBTCxmr = thumbXMRkrw/thumbBTCkrw
	thumbXMRVol = float(xmrjson['data']['volume_1day'])
	stringtosend = "Bithumb last: {0:.6f} BTC on {1:.2f} XMR volume | ".format(thumbBTCxmr,thumbXMRVol)
    except:
	bot.say("Error - bithumb korea is worst korea.")

    # Polo
    try:
	r=requests.get(polourl)
        j=r.json()
        xmr=j["BTC_XMR"]
        last=float(xmr['last'])
#       change=float(xmr['percentChange'])
        vol=float(xmr['baseVolume'])
    	stringtosend += "Poloniex last: {0:.6f} BTC on {1:.2f} BTC volume | ".format(last, vol)
    except:
        bot.say("Something borked ¯\(º_o)/¯")

    # bfx
    try:
        r = requests.get(finexbtc)
        j = r.json()
        stringtosend += "Bitfinex last: {0:.6f} on {1:.2f} XMR volume | ".format(float(j['last_price']), float(j['volume']))
    except:
        bot.say("Something borked ʕノ•ᴥ•ʔノ ︵ ┻━┻")

    # Kraken
    try:
        r = requests.get(krakbtc)
        j = r.json()
        stringtosend += "Kraken last: {0:.6f} on {1:.2f} XMR volume | ".format(float(j['result']['XXMRXXBT']['c'][0]), float(j['result']['XXMRXXBT']['v'][1]))
    except:
        bot.say("Something borked ¤\( `⌂´ )/¤")

    # Binance
    try:
        r = requests.get(binanceurl)
        j = r.json()
        found = False
        for i in j:
            if i["symbol"] == "XMRBTC":
                last=float(i['lastPrice'])
                vol=float(i['volume'])
                stringtosend += ("Binance last: {0:.6f} on {1:.2f} BTC volume | ".format(last, vol*last))
                found = True
    except:
        bot.say("Borka borka ┌∩┐(◣_◢)┌∩┐")

    # Trex
    geturl = trexurl+'xmr'
    try:
        r = requests.get(geturl)
        j = r.json()
        xmr=j['result'][0]
        last=float(xmr['Last'])
#       change=((last/float(xmr['PrevDay']))-1)
        vol=float(xmr['BaseVolume'])
        stringtosend += "Bittrex last: {0:.6f} BTC on {1:.2f} BTC volume | ".format(last, vol)
    except:
        bot.say("Something borked -_-")

    # Cryptopia
    try:
        coin = 'XMR'
        pair = 'BTC'
        r = requests.get(cryptopiaurl)
        j = r.json()
        found = False
        for i in j["Data"]:
            if i["Label"] == coin+"/"+pair:
                last=float(i['LastPrice'])
                change=float(i['Change'])
                vol=float(i['Volume'])
                stringtosend += "Cryptopia last: {0:.6f} {1} on {2:.2f} {1} volume | ".format(last, pair, vol*last)
                found = True
        if found == False:
            bot.say("WTF?!?")
    except:
        bot.say("Something borked （ -.-）ノ-=≡≡卍")

    # Tux
    # try:
    #     r = requests.get('https://tuxexchange.com/api?method=getticker')
    #     j = r.json()
    #     if not trigger.group(2):
    #         ticker='XMR'
    #     else:
    #         ticker=trigger.group(2).upper()
    #     coin=j['BTC_{}'.format(ticker)]
    #     last=float(coin['last'])
    #     vol=float(coin['baseVolume'])
    #     change=float(coin['percentChange'])
    #      stringtosend += "Tux last: {0:.6f} BTC on {1:.2f} BTC volume. ".format(last, vol)
    #  except:
    #      bot.say("Something borked ( ︶︿︶)_╭∩╮")
    #Finally... print to IRC
    bot.say(stringtosend[:-2])


@sopel.module.commands('usd')
def usd(bot, trigger):
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])
        bot.say("Monero price in USD = ${0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")


@sopel.module.commands('price')
def price(bot, trigger):
    try:
        bot.say("1 XMR = $12,345 USD (Offer valid in participating locations)")
    except:
        bot.say("C-cex sucks")

@sopel.module.commands('comm')
def comm(bot, trigger):
    commurl = 'https://api.commoprices.com/v1/wrb/'
    apitoken = '?api_token=9gdRSeoek4N0AnZHUvP0TSIR74jmyQpsjz5HuGRjfDmsCDxppYiG76GuxaF1'
    try:
        r = requests.get(commurl+apitoken)
        data = r.json()['data']
        for i in data:
            if trigger.group(2).lower() in i['name'].lower():
                print(i)
                code = i['code']
    except:
        bot.say("Error getting data or commodity not priced")
        return
    try:
        r2 = requests.get(commurl+code+'/data/'+apitoken)
        j = r2.json()
        bot.say("{0} last price at {1:.2f} {2} on {3}".format(j['data']['info']['name'], j['data']['request']['dataseries'][-1][1], j['data']['info']['original_price_unit']['name'], j['data']['request']['dataseries'][-1][0]))
    except:
        bot.say("Error parsing some shit")

@sopel.module.commands('xmy')
def xmy(bot, trigger):
    try:
        r = requests.get('https://api.coinmarketcap.com/v1/ticker?limit=500')
        j = r.json()
    except:
        bot.say("Can't connect to API")
    symbol = 'XMY'
    try:
        for i in j:
            try:
                if i['symbol'] == symbol:
                    coin = i
            except: pass
            try:
                if i['rank'] == str(rank):
                    coin = i
            except: pass
        symbol = coin['symbol']
        name = coin['name']
        rank = coin['rank']
        price_usd = float(coin['price_usd'])
        price_btc = float(coin['price_btc'])
        volume_usd = float(coin['24h_volume_usd'])
        market_cap_usd = float(coin['market_cap_usd'])
        available_supply = float(coin['available_supply'])
        total_supply = float(coin['total_supply'])
        percent_change_24h = float(coin['percent_change_24h'])
        bot.say("{0} ({1}) is #{2}. Last price ${3:.2f} / ฿{4:.8f}. 24h volume ${5:,.0f} changed {6}%. Market cap ${7:,.0f}. Available / total coin supply {8:,.0f} / {9:,.0f}.".format(name, symbol, rank, price_usd, price_btc, volume_usd, percent_change_24h, market_cap_usd, available_supply, total_supply))
    except:
        bot.say("Error parsing ticker")

@sopel.module.commands('localmonero', 'localxmr', 'lxmr', 'lm', 'street')
def localmonero(bot, trigger):
    try:
        r = requests.get(localmonerousd)
        j = r.json()
        stringtosay = "LocalMonero XMR/USD 12h-avg: ${0:.2f}, 24h-avg: ${0:.2f}.".format(float(j['USD']['avg_12h']), float(j['USD']['avg_24h']))
        bot.say(stringtosay)
    except:
        bot.say("Error getting data")

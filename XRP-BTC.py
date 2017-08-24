import xlwt
import requests
import time

coins = ('BTC','XRP','USD')

intial = float(input("Initial: "))

while True:

	#BTCMARKETS
	btcmarketsAUD = {}
	for coin in coins:
		#data
		if coin == 'BTC':
			url = "https://api.btcmarkets.net/market/" + coin + "/AUD/tick"
			r = requests.get(url, verify=True)
			btcmarketsAUD["{0}".format(coin)] = float(r.json()["lastPrice"])
		elif coin == 'XRP':
			url = "https://api.btcmarkets.net/market/" + coin + "/AUD/tick"
			r = requests.get(url, verify=True)
			btcmarketsAUD["{0}".format(coin)] = float(r.json()["lastPrice"])
		
	print("BTCMARKETS")
	print(btcmarketsAUD)

	#BITFINEX
	bitfinexBTC = {}
	for coin in coins:
		#data 
		if coin == 'USD':
			url = "https://api.bitfinex.com/v1/pubticker/BTC" + coin
			r = requests.get(url, verify=True)
			bitfinexBTC["{0}".format(coin)] = float(r.json()["last_price"])
		elif coin == 'XRP':
			url = "https://api.bitfinex.com/v1/pubticker/" + coin + "BTC"
			r = requests.get(url, verify=True)
			bitfinexBTC["{0}".format(coin)] = float(r.json()["last_price"])
		
		
		
	print("BITFINEX")
	print(bitfinexBTC)


	#FEES AXRP --> UXRP --> UBTC --> ABTC
	fixedBTCFee = (0.0004 * bitfinexBTC["USD"])
	fixedXRPFee = (0.15 * btcmarketsAUD["XRP"])

	feesBTCBuy = (intial * 0.0085)
	feeBTCBFX = (intial - (feesBTCBuy + fixedXRPFee)) * 0.002
	feesBTCSell = (intial - (feesBTCBuy + feeBTCBFX + fixedXRPFee + fixedBTCFee)) * 0.0085

	feesTotal = feesBTCBuy + feeBTCBFX + fixedXRPFee + fixedBTCFee + feesBTCSell
	print("Fees: " + str("{0:.2f}".format(feesTotal)))

	#FINAL WITHOUT FEES
	final = float(intial/ btcmarketsAUD["XRP"]  * bitfinexBTC['XRP'] * btcmarketsAUD["BTC"])
	print("Final: " + str("{0:.2f}".format(final)))

	#FINAL WITH FEES
	finalWithFees = final - feesTotal
	print("Final with Fees: " + str("{0:.2f}".format(finalWithFees)))

	#PERCENTAGE
	percentage = "{0:.2f}".format(finalWithFees / intial * 100)
	print("Percentage: " + str(percentage) + "%")

	f = open('ExchangeLogXRP-BTC.txt', 'a')
	f.write(str(time.strftime("%c", time.localtime())) + " " + "{0:.2f}".format(finalWithFees) + " " + str(percentage) + "%  \n")
	f.close()

	print("\n")
	time.sleep(60)

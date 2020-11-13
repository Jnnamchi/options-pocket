import requests
import yfinance as yf
import json
import datetime
import numpy as np
import pandas as pd

def getAllData(ticker):

	# Company Basic Data
	company = yf.Ticker(ticker)
	companyInfo = company.info
	companyHistoryDF = company.history(start="2010-01-01")
	historicalPricing = getHistoricalPrices(companyHistoryDF)

	# # Options Data
	optionsData = getOptionsData(company, ticker)

	return json.dumps({
		"historicalPricing": historicalPricing,
		"optionsData": optionsData,
		"priceData": {
			"name": companyInfo["shortName"],
			"website": companyInfo["website"],
			"bid": companyInfo["bid"],
			"ask": companyInfo["ask"],
			"volume": companyInfo["volume"],
		}
	})

def getHistoricalPrices(companyHistoryDF):
	historicalPricing = []
	for row in companyHistoryDF.itertuples():
		# print(row)
		dataPoint = {
			"x": row.Index.to_pydatetime().strftime("%Y-%m-%d"),
			"y": round(((row.Open + row.Close) / 2), 2)
		}
		historicalPricing.append(dataPoint)

	return historicalPricing


##########################################
#                                        #
#            All Options Data            #
#                                        #
##########################################


def getOptionsData(company, ticker):
	optionsChain = getOptionsChains(company)
	volatilityHistory = getVolatilityHistory(ticker)

	return {
		"volatilityHistory": volatilityHistory,
		"optionsChain": optionsChain,
	}

def getOptionsChains(company):
	optionsChains = {}

	for expiryDate in company.options:
		optionChain = company.option_chain(expiryDate)

		allCalls = []
		for call in optionChain.calls.itertuples():
			allCalls.append({
				"ask": call.ask if call.ask == call.ask else 0,
				"bid": call.bid if call.bid == call.bid else 0,
				# "change": call.change,
				# "contractSize": call.contractSize,
				"contractSymbol": call.contractSymbol,
				# "currency": call.currency,
				"impliedVolatility": call.impliedVolatility,
				# "inTheMoney": call.inTheMoney,
				"lastPrice": call.lastPrice,
				# # "lastTradeDate": call.lastTradeDate,
				# "openInterest": call.openInterest,
				# "percentChange": call.percentChange,
				"strike": call.strike,
				# "volume": call.volume,
			})

		allPuts = []
		for put in optionChain.puts.itertuples():
			allPuts.append({
				"ask": put.ask if put.ask == put.ask else 0,
				"bid": put.bid if put.bid == put.bid else 0,
				# "change": put.change,
				# "contractSize": put.contractSize,
				"contractSymbol": put.contractSymbol,
				# "currency": put.currency,
				"impliedVolatility": put.impliedVolatility,
				# "inTheMoney": put.inTheMoney,
				"lastPrice": put.lastPrice,
				# # "lastTradeDate": put.lastTradeDate,
				# "openInterest": put.openInterest,
				# "percentChange": put.percentChange,
				"strike": put.strike,
				# "volume": put.volume,
			})

		optionsChains[expiryDate] = {
			"calls": allCalls,
			"puts": allPuts,
		}

	return optionsChains

def getVolatilityHistory(ticker):

	# Good Resrouces:
	# https://www.projectoption.com/historical-volatility-options-traders/

	# This gets the historical volatility scores
	meanImpliedVolatility = requests.get("https://www.alphaquery.com/data/option-statistic-chart?ticker=" + ticker + "&perType=30-Day&identifier=iv-mean")
	meanImpliedVolatility = json.loads(meanImpliedVolatility.text)
	meanImpliedVolatility = formatDataPoints(meanImpliedVolatility, "value", "y")

	historicalVolatility = requests.get("https://www.alphaquery.com/data/option-statistic-chart?ticker=" + ticker + "&perType=30-Day&identifier=historical-volatility")
	historicalVolatility = json.loads(historicalVolatility.text)
	historicalVolatility = formatDataPoints(historicalVolatility, "value", "y")

	return {
		"IV": meanImpliedVolatility,
		"HV": historicalVolatility
	}

def getOptionQuote(contractSymbol):
	rawOptionQuote = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/" + contractSymbol + "?region=US&lang=en-US&includePrePost=false&interval=1d&range=3mo&corsDomain=finance.yahoo.com&.tsrc=finance")
	rawOptionQuote = json.loads(rawOptionQuote.text)

	result = rawOptionQuote["chart"]["result"][0]

	historicalData = []
	for i in range(len(result["timestamp"])):

		if len(result["indicators"]["quote"]) != 1:
			continue

		quote = result["indicators"]["quote"][0]

		closePrice = quote["close"][i]
		openPrice = quote["open"][i]

		if (openPrice == None or closePrice == None):
			continue

		timestamp = result["timestamp"][i]

		dataPoint = {
			"x": datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d"),
			"y": round(((openPrice + closePrice) / 2), 2)
		}
		historicalData.append(dataPoint)

	finalOptionQuote = {
		"contractSymbol": result["meta"]["symbol"],
		"historicalData": historicalData
	}

	return finalOptionQuote

##########################################
#                                        #
#           General Formatting           #
#                                        #
##########################################

def formatDataPoints(array, oldKeyName, newKeyName):

	for obj in array:
		obj[newKeyName] = obj[oldKeyName]
		obj.pop(oldKeyName, None)

		obj["x"] = obj["x"].split("T")[0]

	return array
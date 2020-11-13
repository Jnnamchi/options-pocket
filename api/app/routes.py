from app import app
from flask import request
from flask_cors import CORS

from . import dataCollector

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def index():
	# Get auth token
	ticker = request.args.get('ticker')

	return dataCollector.getAllData(ticker)

@app.route('/options-quote', methods=['GET'])
def getOptionQuote():
	# Get auth token
	contractSymbol = request.args.get('contractSymbol')

	return dataCollector.getOptionQuote(contractSymbol)

<template>
  <div>
    <div class="mainDataHolder">
      <div class="callPutsColumn">
        <div class="callPutTitle">
          CALLS
        </div>
        <div class="expiryDateRange">
          <span v-for="expiry in Object.keys(companyData.optionsData.optionsChain)"
                v-bind:key="expiry"
                class="expirySelect"
                v-on:click="setOptionChain(companyData.optionsData.optionsChain[expiry], expiry)"
                :style="formatExpiryDate(expiry)">
            {{expiry}}
          </span>
        </div>
        <div class="callPutsRowHeading">
          <div class="columnTitle">
            Bid
          </div>
          <div class="columnTitle">
            Ask
          </div>
          <div class="columnTitle">
            Last
          </div>
          <div class="columnTitle">
            IV
          </div>
          <div class="columnTitle strikeCell">
            Strike
          </div>
        </div>
        <div class="selectedChainContainer">
          <div
          v-for="call in selectedCallOptionsChain"
          v-bind:key="call.strike"
          class="callPutsRow"
          v-on:click="getOptionQuote(call, selectedExpiryDate)"
          :style="formatSelectedOption(call.contractSymbol)">
            <div>
              {{call.bid.toFixed(2)}}
            </div>
            <div>
              {{call.ask.toFixed(2)}}
            </div>
            <div>
              {{call.lastPrice.toFixed(2)}}
            </div>
            <div>
              {{(100*call.impliedVolatility).toFixed(2)}}
            </div>
            <div class="strikeCell">
              {{call.strike.toFixed(2)}}
            </div>
          </div>
        </div>
      </div>
      <div>
        <!-- <h1>{{ msg }}</h1> -->
        <!-- <div>
          Strategy:
          <div>
            - SELL an overpriced option when IV RANK is HIGH to get good premiums, that has high likelihood of expiring worthless
          </div>
          <div>
            - BUY an underpriced option when IV RANK is LOW, especially if potential for future price movement is high
          </div>
        </div> -->
        <div>
          <input class="selectCompanyInput" v-model="ticker">
          <button class="selectCompanyButton" v-on:click="getCompanyData(ticker)">GO!</button>
        </div>
        <div class="selectedCompanyContainer">
          <div class="selectedCompanyVisual">
            <div class="selectedCompanyLogo">
              <img class="selectedCompanyLogoImage" :src="'//logo.clearbit.com/' + companyData.priceData.website">
            </div>
            <div class="selectedCompanyName">
              {{companyData.priceData.name}}
            </div>
            <div class="selectedCompanyWebsite">
                <a :href="companyData.priceData.website" target="_blank">Website</a>
            </div>
          </div>
          <div class="selectedCompany">
            <div class="selectedCompanyInfo">
              <div>
                {{companyData.priceData.bid.toFixed(2)}}
              </div>
              <div>
                {{companyData.priceData.ask.toFixed(2)}}
              </div>
              <div>
                {{companyData.priceData.last.toFixed(2)}}
              </div>
              <div>
                {{(100*companyData.priceData.IV).toFixed(2)}}
              </div>
              <div>
                {{companyData.priceData.IVRank.toFixed(2)}}
              </div>
              <div>
                {{companyData.priceData.IVPercentile.toFixed(2)}}
              </div>
              <div>
                {{formatNumber(companyData.priceData.volume)}}
              </div>
              <div>
                {{companyData.priceData.volumeRank.toFixed(2)}}
              </div>
            </div>
            <div class="selectedCompanyInfoLegend">
              <div class="columnTitle">
                Bid
              </div>
              <div class="columnTitle">
                Ask
              </div>
              <div class="columnTitle">
                Last
              </div>
              <div class="columnTitle">
                IV
              </div>
              <div class="columnTitle">
                IV RANK
              </div>
              <div class="columnTitle">
                IV %
              </div>
              <div class="columnTitle">
                Vol
              </div>
              <div class="columnTitle">
                Vol Rank
              </div>
            </div>
          </div>
        </div>
        <div class="canvasContainer">
          <canvas class="mainChartData" id="mainChart"></canvas>
        </div>
        <div class="canvasContainer">
          <canvas class="optionsPrice" id="optionsPrice"></canvas>
        </div>
      </div>
      <div class="callPutsColumn">
        <div class="callPutTitle">
          PUTS
        </div>
        <div class="expiryDateRange">
          <span v-for="expiry in Object.keys(companyData.optionsData.optionsChain)"
                v-bind:key="expiry"
                class="expirySelect"
                v-on:click="setOptionChain(companyData.optionsData.optionsChain[expiry], expiry)"
                :style="formatExpiryDate(expiry)">
            {{expiry}}
          </span>
        </div>
        <div class="callPutsRowHeading">
          <div class="columnTitle strikeCell">
            Strike
          </div>
          <div class="columnTitle">
            Bid
          </div>
          <div class="columnTitle">
            Ask
          </div>
          <div class="columnTitle">
            Last
          </div>
          <div class="columnTitle">
            IV
          </div>
        </div>
        <div class="selectedChainContainer">
          <div v-for="put in selectedPutOptionsChain"
          v-bind:key="put.strike"
          class="callPutsRow"
          v-on:click="getOptionQuote(put, selectedExpiryDate)"
          :style="formatSelectedOption(put.contractSymbol)">
            <div class="strikeCell">
              {{put.strike.toFixed(2)}}
            </div>
            <div>
              {{put.bid.toFixed(2)}}
            </div>
            <div>
              {{put.ask.toFixed(2)}}
            </div>
            <div>
              {{put.lastPrice.toFixed(2)}}
            </div>
            <div>
              {{(100*put.impliedVolatility).toFixed(2)}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios to make requests
import axios from 'axios'

// Import ChartJS
import Chart from 'chart.js';
import 'chartjs-plugin-crosshair'

export default {
  name: 'StockCharter',
  props: {
    msg: String
  },
  data () {
    return {
      ticker: "AAPL",
      scatterChart: {},
      optionsPriceChart: {},
      companyData: {
        optionsData: {
          optionsChain: {},
        },
        priceData: {
          name: "Company Name",
          website: "https://www.youtube.com",
          bid: 0.00,
          ask: 0.00,
          last: 0.00,
          IV: 0.00,
          IVRank: 0.00,
          IVPercentile: 0.00,
          volume: 0.00,
          volumeRank: 0.00,
        },
      },
      // Specific Datasets to add
      priceForecastData: {
        "SD1": {
          "above": [],
          "below": [],
        },
        "SD2": {
          "above": [],
          "below": [],
        },
        "SD3": {
          "above": [],
          "below": [],
        },
      },
      zoomDateFilters: {
        "start": "",
        "end": "",
      },
      selectedExpiryDate: "",
      selectedOptionContract: "",
      selectOptionHistoricalData: [],
      selectedCallOptionsChain: [],
      selectedPutOptionsChain: [],
      selectedOption: {},
      selectedOptionDataPoint: {},
    }
  },
  mounted () {
    this.initializeChart()
    this.getCompanyData("AAPL")
  },
  methods: {
    getCompanyData (ticker) {
      let requestURL = "http://localhost:5000/?ticker=" + ticker
      axios.get(requestURL)
      .then(response => {
        // Replace all chart data with new data
        let selectedCompanyData = response.data
        this.updateChart(response.data.historicalPricing)

        let lastEntry = response.data.historicalPricing[response.data.historicalPricing.length-1]
        let lastPrice = lastEntry.y
        let lastDate = lastEntry.x

        this.zoomDateFilters.end = lastEntry.x
        this.zoomDateFilters.start = response.data.historicalPricing[0].x

        // Graph the volatility history (IV)
        let lastIV = response.data.optionsData.volatilityHistory.IV[response.data.optionsData.volatilityHistory.IV.length - 1].y
        this.setFuturePriceRanges(lastPrice, lastDate, lastIV, Object.keys(response.data.optionsData.optionsChain))

        let [ivRank, ivPercentile] = this.getIVRankPercentile(lastIV, response.data.optionsData.volatilityHistory.IV)

        selectedCompanyData.priceData.IV = lastIV
        selectedCompanyData.priceData.IVRank = ivRank
        selectedCompanyData.priceData.IVPercentile = ivPercentile
        selectedCompanyData.priceData.last = lastPrice
        selectedCompanyData.priceData.volumeRank = 0

        this.companyData = selectedCompanyData
        console.log(response.data)

        // Setup the options
        let closestCallOptionDate = Object.keys(response.data.optionsData.optionsChain)[0]
        this.selectedExpiryDate = closestCallOptionDate

        this.selectedCallOptionsChain = response.data.optionsData.optionsChain[closestCallOptionDate].calls
        this.selectedPutOptionsChain = response.data.optionsData.optionsChain[closestCallOptionDate].puts
        let closestOption = {}
        for (let call of this.selectedCallOptionsChain) {
          if (call.strike > lastPrice) {
            closestOption = call
            this.selectedOption = closestOption
            this.selectedOptionContract = closestOption.contractSymbol
            this.getOptionQuote(closestOption, this.selectedExpiryDate)
            return
          }
        }
      }).catch(error => {
        if (error) {
          console.log("There was an error")
          console.log(error)
        }
        alert("Error fetching data")
      })
    },
    initializeChart () {
      // Init Scatter Chart
      let ctx = document.getElementById("mainChart").getContext('2d')
      this.scatterChart = new Chart(ctx, {
        type: 'scatter',
        data: {
          datasets: [],
        },
        options: {
          legend: {
            display: false
          },
          tooltips: {
            mode: 'interpolate',
            intersect: false,
            callbacks: {
              title: function(a) {
                return new Date(a[0].xLabel).toISOString().split('T')[0]
              },
              label: function(i, d) {
                return (
                  d.datasets[i.datasetIndex].label + ": " + i.yLabel.toFixed(2)
                );
              }
            },
          },
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
              }
            }],
            xAxes: [{
              type: "time",
              time: {
                parser: "YYYY-MM-DD",
                tooltipFormat: 'll',
                label: "month",
              },
            }]
          },
          plugins: {
            crosshair: {
              callbacks: {
                afterZoom: (start, end) => {
                  setTimeout(() => {
                    this.updateChartOnZoom(this.companyData.historicalPricing, start, end)
                  }, 10)
                }
              }
            }
          },
        },
      })
      // Init Options Chart
      let ctx2 = document.getElementById("optionsPrice").getContext('2d')
      this.optionsPriceChart = new Chart(ctx2, {
        type: 'scatter',
        data: {
          datasets: [],
        },
        options: {
          legend: {
            display: false
          },
          tooltips: {
            mode: 'interpolate',
            intersect: false,
          },
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
              }
            }],
            xAxes: [{
              type: "time",
              time: {
                parser: "YYYY-MM-DD",
                tooltipFormat: 'll',
                unit: 'day'
              },
              ticks: {
                beginAtZero: true,
              }
            }]
          }
        },
      })
    },
    updateChart(chartData) {
      let newData = [{
        label: 'Scatter Dataset',
        showLine: true,
        data: chartData,
        pointRadius: 0,
      }]
      this.scatterChart.config.data.datasets = newData
      this.scatterChart.update()
    },
    updateChartOnZoom (chartData, startDate, endDate) {
      let filteredData = this.filterDataSetByDate(chartData, startDate, endDate)
      let newData = [{
        label: 'Scatter Dataset',
        showLine: true,
        data: filteredData,
        pointRadius: 0,
      }]
      this.scatterChart.config.data.datasets = newData
      this.scatterChart.update()
      this.addForecastData()

      this.addSelectedOptionToChart(this.selectedOptionDataPoint)

      // Re-add the options data to the options chart
      this.updateOptionsPriceChart(this.selectOptionHistoricalData)

      // Re-add the current selected option data
    },
    filterDataSetByDate (dataset, startDate, endDate) {
      let filteredData = []
      for (let data of dataset) {
        if (new Date(data.x) >= startDate.toDate() && new Date(data.x) <= endDate.toDate()) {
          filteredData.push(data)
        }
      }
      return filteredData
    },
    setOptionChain(optionsChain, expiryDate) {
      this.selectedExpiryDate = expiryDate
      this.selectedCallOptionsChain = optionsChain.calls
      this.selectedPutOptionsChain = optionsChain.puts
    },
    formatExpiryDate(expiryDate) {
      if (expiryDate == this.selectedExpiryDate) {
        return "background-color: #4287f5; cursor: pointer; color: white;"
      }
      return ""
    },
    formatSelectedOption(optionContract) {
      if (optionContract == this.selectedOptionContract) {
        return "background-color: red; color: white;"
      }
      return ""
    },
    getOptionQuote(option, selectedExpiryDate) {
      let requestURL = "http://localhost:5000/options-quote?contractSymbol=" + option.contractSymbol
      axios.get(requestURL)
      .then(response => {
        // console.log("OPTION QUOTE:")
        // console.log(response.data)
        this.selectedOptionContract = response.data.contractSymbol
        this.selectOptionHistoricalData = response.data.historicalData
        this.updateOptionsPriceChart(this.selectOptionHistoricalData)
        let newDataPoint = {
          "x": selectedExpiryDate,
          "y": option.strike,
        }
        this.addSelectedOptionToChart(newDataPoint)
      }).catch(error => {
        if (error) {
          console.log("There was an error")
          console.log(error)
        }
        alert("Error fetching data")
      })
    },
    addSelectedOptionToChart (dataPoint) {
      this.selectedOptionDataPoint = dataPoint
      let newData = {
        label: "selectedOption",
        data: [dataPoint],
        showLine: false,
        pointRadius: 5,
        pointBackgroundColor: "green",
        fill: false,
        borderColor: "green",
        borderWidth: 1,
      }
      for (let i = 0; i < this.scatterChart.data.datasets.length; i++) {
        if (this.scatterChart.data.datasets[i].label == "selectedOption") {
          this.scatterChart.data.datasets.splice(i, 1)
        }
      }
      this.scatterChart.data.datasets.push(newData)
      this.scatterChart.update()
    },
    updateOptionsPriceChart (chartData) {
      let newData = [{
        pointHitRadius: 200,
        pointRadius: 0,
        fill: false,
        label: 'Scatter Dataset',
        showLine: true,
        data: chartData,
      }]
      this.optionsPriceChart.config.data.datasets = newData
      this.optionsPriceChart.update()
    },
    // Set Future Predicted Ranges
    setFuturePriceRanges(lastPrice, lastDate, IV, expiryDates) {
      let aboveValuesSD1 = [{"x": lastDate, "y": lastPrice}], aboveValuesSD2 = [{"x": lastDate, "y": lastPrice}], aboveValuesSD3 = [{"x": lastDate, "y": lastPrice}]
      let belowValuesSD1 = [{"x": lastDate, "y": lastPrice}], belowValuesSD2 = [{"x": lastDate, "y": lastPrice}], belowValuesSD3 = [{"x": lastDate, "y": lastPrice}]
      let total = 0
      for (let expiryDate of expiryDates) {
        total++
        if (total > 10) {
          continue
        }
        let daysUntilExpiry = new Date(expiryDate) - new Date()
        let res = Math.abs(daysUntilExpiry) / 1000
        let daysUntil = (Math.floor(res / 86400)) + 1
        let correctValue = (lastPrice*IV*Math.sqrt(daysUntil/365))
        aboveValuesSD1.push({
          "x": expiryDate,
          "y": lastPrice + correctValue
        })
        aboveValuesSD2.push({
          "x": expiryDate,
          "y": lastPrice + 2*correctValue
        })
        aboveValuesSD3.push({
          "x": expiryDate,
          "y": lastPrice + 3*correctValue
        })
        // Below Values - min of 0 or the value
        belowValuesSD1.push({
          "x": expiryDate,
          "y": Math.max(lastPrice - correctValue, 0)
        })
        belowValuesSD2.push({
          "x": expiryDate,
          "y": Math.max(lastPrice - 2*correctValue, 0)
        })
        belowValuesSD3.push({
          "x": expiryDate,
          "y": Math.max(lastPrice - 3*correctValue, 0)
        })
      }
      this.priceForecastData = {
        "SD1": {
          "above": aboveValuesSD1,
          "below": belowValuesSD1,
        },
        "SD2": {
          "above": aboveValuesSD2,
          "below": belowValuesSD2,
        },
        "SD3": {
          "above": aboveValuesSD3,
          "below": belowValuesSD3,
        },
      }
      this.addForecastData()
    },
    addForecastData () {
      this.updateMainChartWithForecastData(this.priceForecastData.SD1.above)
      this.updateMainChartWithForecastData(this.priceForecastData.SD2.above)
      this.updateMainChartWithForecastData(this.priceForecastData.SD3.above)
      this.updateMainChartWithForecastData(this.priceForecastData.SD1.below)
      this.updateMainChartWithForecastData(this.priceForecastData.SD2.below)
      this.updateMainChartWithForecastData(this.priceForecastData.SD3.below)
    },
    updateMainChartWithForecastData(theData) {
      let newData = {
        data: theData,
        showLine: true,
        pointRadius: 1,
        pointBackgroundColor: "blue",
        fill: false,
        borderColor: "blue",
        borderWidth: 1,
      }
      this.scatterChart.data.datasets.push(newData)
      this.scatterChart.update()
    },
    formatNumber(x) {
      if (isNaN(x) || x < 9999) {
        return x
      }
      if (x < 1000000) {
        return Math.round(x/1000) + "K"
      }
      if( x < 10000000) {
        return (x/1000000).toFixed(2) + "M"
      }
      if (x < 1000000000) {
        return Math.round((x/1000000)) + "M"
      }
      if (x < 1000000000000) {
        return Math.round((x/1000000000)) + "B"
      }
      return "1T+";
    },
    getIVRankPercentile (value, historicalIV) {
      let max = 0
      let min = 10000
      let numberOfTimesBelow = 0
      for (let IV of historicalIV) {
        let IvValue = IV.y
        if (IvValue > max) {
          max = IvValue
        }
        if (IvValue < min) {
          min = IvValue
        }
        if (IvValue < value) {
          numberOfTimesBelow++
        }
      }

      console.log("MAX IS")
      console.log(max)
      console.log(min)
      console.log(value)

      let ivRank = 100 * (value - min) / (max - min)
      let ivPercentile = (100 * numberOfTimesBelow) / historicalIV.length
      return [ivRank, ivPercentile]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.mainChartData {
  max-width: 100%;
  max-height: 600px;
  margin: 20px auto;
}
.optionsPrice {
  max-width: 80%;
  max-height: 400px;
  margin: 50px auto;
}
.mainDataHolder {
  display: grid;
  grid-template-columns: auto auto auto;
  column-gap: 40px;
  width: 98%;
  margin: 0 auto;
}
.callPutsColumn {
  max-width: 361px;
}
.selectCompanyInput {
  border: none;
  border-bottom: solid blue 1px;
  width: 85px;
  margin-right: 20px;
}
.selectCompanyButton {
  background-color: white;
  border: none;
  color: blue;
  padding: 5px 10px;
  border-radius: 4px;
}
.selectCompanyButton:hover {
  cursor: pointer;
  background-color: blue;
  border: none;
  color: white;
  padding: 5px 10px;
}
.selectedCompanyContainer {
  display: grid;
  grid-template-columns: 200px auto;
  width: fit-content;
  margin: 0 auto;
  column-gap: 40px;
}
.selectedCompanyVisual {
  margin-top: 0;
}
.selectedCompanyLogo {
  width: 80px;
  height: 80px;
  margin: 20px auto 10px;
}
.selectedCompanyLogoImage {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.selectedCompanyName {
  font-size: 23px;
  font-weight: bold;
}
.selectedCompanyWebsite {
  color: blue;
  font-size: 11px;
  margin-top: 5px;
}
.selectedCompanyInfo {
  display: grid;
  grid-template-columns: 80px 80px 80px 80px 80px 80px 80px 80px;
  line-height: 45px;
  text-align: center;
  width: fit-content;
  margin: 30px auto 0 auto;
  font-size: 18px;
  font-weight: bold;
}
.selectedCompanyInfoLegend {
  display: grid;
  grid-template-columns: 80px 80px 80px 80px 80px 80px 80px 80px;
  line-height: 35px;
  text-align: center;
  width: fit-content;
  margin: 5px auto 0 auto;
}
.selectedChainContainer {
  height: 600px;
  overflow: scroll;
  border: solid black 1px;
  width: fit-content;
}
.callPutTitle {
  font-size: 22px;
}
.callPutsRow {
  display: grid;
  grid-template-columns: 72px 72px 72px 72px 72px;
  line-height: 50px;
  text-align: center;
  width: fit-content;
  border-bottom: solid black 1px;
  font-size: 14px;
}
.callPutsRow:hover {
  cursor: pointer;
  background-color: #ddd;
}
.callPutsRowHeading {
  display: grid;
  grid-template-columns: 72px 72px 72px 72px 72px;
  line-height: 50px;
  text-align: center;
  width: fit-content;
  border: solid black 1px;
}
.columnTitle {
  color: grey;
  font-size: 14px;
}
.expiryDateRange {
  display: flex;
  flex-wrap: wrap;
  margin: 20px 0;
}
.expirySelect {
  font-size: 12px;
  word-break: keep-all;
  margin: 5px;
  max-width: 100px !important;
  padding: 3px 5px;
  border-radius: 5px;
  font-weight: bold;
}
.expirySelect:hover {
  background-color: #4287f5;
  cursor: pointer;
  color: white;
}
.strikeCell {
  background-color: #4287f5;
  color: white;
  font-weight: bold;
}
.canvasContainer {
  position: relative;
}
.reset-zoom {
  color: grey;
  position: absolute;
  right: 0;
  top: 0;
  margin-right: 7%;
  margin-top: 20px;
  border: none;
  background: none;
}
.reset-zoom:hover {
  color: blue;
  cursor: pointer;
}
</style>

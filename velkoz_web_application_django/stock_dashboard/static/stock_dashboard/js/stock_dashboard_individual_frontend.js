// Extracting data from HTML document:
const priceHistoryIndexElement = document.getElementById('priceHistoryIndex');
const priceHistoryCloseElement = document.getElementById('priceHistoryClose');
const pricePctChangeCloseElement = document.getElementById('priceHistoryClose');
const priceCumSumCloseElement = document.getElementById('priceCumSumClose');
const price30DStdElement = document.getElementById('price30DayStd');

// Converting extracted data to json format:
var priceHistoryIndex = JSON.parse(priceHistoryIndexElement.textContent);
var priceHistoryClose = JSON.parse(priceHistoryCloseElement.textContent);
var pricePctChangeClose = JSON.parse(pricePctChangeCloseElement.textContent);
var priceCumSumClose = JSON.parse(priceCumSumCloseElement.textContent);
var price30DayStd = JSON.parse(price30DStdElement.textContent);

// Creating the Price Time-Series Data Context:
var priceHistoryCtx = [{
	type: 'scatter',
	mode: 'lines',
	name: 'Price History',
	x: priceHistoryIndex,
	y: priceHistoryClose
}];

// Generating the Plot for Price History Time-Series:
Plotly.newPlot('priceTimeSeries', priceHistoryCtx, {
	height: 450,
	title: {
		text: `Closing Price History of ${ticker}`
	},
	xaxis: {
		title: {
			text: "Time-Series (dd-mm-yyyy)"
		},
		tickformat: "%d-%m-%Y",
		type: 'date'
	},
	yaxis: {
		title: {
			text: "Closing Price ($)"
		}
	}
});


// Creating the Price Percent Change Historgram Context:
var pricePctChangeCtx = [{
	x: pricePctChangeClose,
	type: 'histogram'
}];

// Generating the Plot for the Price Percent Change Historgram:
Plotly.newPlot('pricePctChangeHist', pricePctChangeCtx, {
	bargap: 0.05,
	title: "Price Percent Change Historgram"
}); 


// Creating the Cummulative Returns Time-Series Context:
var priceCumSumCtx = [{
	type: 'scatter',
	mode: 'lines',
	name: 'Cummulative Returns',
	x: priceHistoryIndex,
	y: priceCumSumClose
}];

// Generating the Plot for the Cummulative Returns Time Series:
Plotly.newPlot('priceCummulativeReturnsTimeSeries', priceCumSumCtx , {
		height: 450,
	title: {
		text: `Historical Cummulative Returns of ${ticker}`
	},
	xaxis: {
		title: {
			text: "Time-Series (dd-mm-yyyy)"
		},
		tickformat: "%d-%m-%Y",
		type: 'date'
	},
	yaxis: {
		title: {
			text: "Find Lable"
		}
	}
});


// Creating the 30 Day Standard Deviation Time-Series Context:
price30DayStdCtx = [{
	type: 'scatter',
	mode: 'lines',
	name: '30 Day Standard Deviation',
	x: priceHistoryIndex,
	y: price30DayStd
}];

Plotly.newPlot('price30DStdTimeSeries', price30DayStdCtx, {
		height: 450,
	title: {
		text: `30-Day Standard Deviation of ${ticker} Prices`
	},
	xaxis: {
		title: {
			text: "Time-Series (dd-mm-yyyy)"
		},
		tickformat: "%d-%m-%Y",
		type: 'date'
	},
	yaxis: {
		title: {
			text: "Price Change (%)"
		}
	}
});




// Declaring JSON values from HTML document:
var priceHistoryIndex = JSON.parse(
	document.getElementById('price_history_index').textContent);
var priceHistoryClose = JSON.parse(
	document.getElementById('price_history_close').textContent);
console.log(priceHistoryClose);

// Creating the Price Time-Series Data Context:
var priceHistoryCTX = [{
	type: 'scatter',
	mode: 'lines',
	name: 'Price History',
	x: priceHistoryIndex,
	y: priceHistoryClose
}];

// Generating the Plot for Price History Time-Series:
Plotly.newPlot('priceTimeSeries', priceHistoryCTX, {
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
// Initialize chart
// 

var chart_height = document.getElementById('chart').offsetHeight;
var chart_width =  document.getElementById('chart').offsetWidth;
console.log ('test');
console.log(chart_width);




var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	priceScale: { autoScale: true},
	width: chart_width-10,
    height: chart_height-10,
	layout: {
		backgroundColor: '#FFFFFF', 
		textColor:'#000000' ,
	},
	grid: {
		vertLines: {
			color: 'rgba(255, 255, 255, 255)',
		},
		horzLines: {
			color: 'rgba(255, 255, 255, 255)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
});

var candleSeries = chart.addCandlestickSeries({
  upColor: 'rgb(0, 163, 108)',
  downColor: 'rgb(255,0,0)',
  borderDownColor: 'rgb(255,0,0)',
  borderUpColor: 'rgb(0, 163, 108)',
  wickDownColor: 'rgb(255,0,0)',
  wickUpColor: 'rgb(0, 163, 108)',
});


var base_url = 'http://'+ app_host + ':'+ app_port + '/history';
console.log(app_host);


fetch(base_url)

	.then((r) => r.json())
	.then((response) => {
          //console.log(response)

		  candleSeries.setData(response);

	})

/* */

//var binancesocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_15m");




binancesocket.onmessage =function(event) {
	var message = JSON.parse(event.data)

	var candlestick = message.k;
	

	candleSeries.update({
       
		time: candlestick.t / 1000,
		open: candlestick.o, 
		high: candlestick.h,
		low:  candlestick.l,
		close: candlestick.c

         

	})
}
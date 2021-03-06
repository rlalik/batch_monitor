// find all keys with given value in object

var update_period_ms = 60000;

function getObjects(obj, key, val) {
	var objects = [];
	for (var i in obj) {
		if (!obj.hasOwnProperty(i)) continue;
		if (typeof obj[i] == 'object') {
			objects = objects.concat(getObjects(obj[i], key, val));
		} else if (i == key && obj[key] == val) {
			objects.push(obj);
		}
	}
	return objects;
}

// configure periodical update of the time chart
function time_chart_updater(subpath, chart, chart_data_type) {
	var f = function() {
		if (chart.series.length) {
			var keys = chart.series[0].xData;
			var last = keys[keys.length-1];
			lastts = last;
		}
		else
			lastts=null

		$.getJSON(subpath+'json/'+chart_data_type+'/?lastts='+lastts+'&callback=?', function(jsondata) {
			if (jsondata == null)
				return

			var s_len = jsondata.result.length;
			if (s_len == 0)
				return;

			var s_len = chart.series.length;
			for (_i = s_len; _i > 0; _i--) {
				var i = _i-1;
				var res = getObjects(jsondata.result, 'name', chart.series[i].name)
				if (res.length == 1) {
					for (j = 0; j < res[0].data.length; j++) {
						chart.series[i].addPoint(res[0].data[j], false, (chart.series[i].data.length >= parseInt(jsondata.limit)) );
					}
					// fix color of the series
					chart.series[i].update({
						color: Highcharts.getOptions().colors[ res[0]._color ],
						zIndex: res[0].zIndex,
						index: res[0].index,
					})
					jsondata.result.splice(jsondata.result.indexOf(res[0]), 1)
				}
				else if (res.length > 1) { }
				else { chart.series[i].remove() }
			}

			var s_len = jsondata.result.length;
			for (i = 0; i < s_len; i++) {
				var ser = chart.addSeries(jsondata.result[i]);
				// fix color of the series
				ser.update({
					color: Highcharts.getOptions().colors[ jsondata.result[i]._color ],
					zIndex: jsondata.result[i].zIndex,
					index: jsondata.result[i].index,
				})
			}
			chart.redraw();
		});
		
		chart_time_subtitle(chart)
	}

	f();
	chart._reflow = function() {
		chart.reflow();
	}

	chart_time_subtitle(chart)

	// set up the updating of the chart each second
	setInterval(function() {f()}, update_period_ms);
}

// configure periodical update of the hist chart
function hist_chart_updater(subpath, chart, chart_data_type) {
	var f = function() {
		$.getJSON(subpath+'json/'+chart_data_type+'/?callback=?', function(jsondata) {
			if (jsondata == null)
				return

			var s_len = jsondata.result.length;
			if (s_len == 0)
				return;

			var s_len = chart.series.length;
			for (_i = s_len; _i > 0; _i--) {
				var i = _i-1;
				var res = getObjects(jsondata.result, 'name', chart.series[i].name)

				if (res.length == 1) {
					chart.series[i].setData(res[0].data);
					chart.series[i].update({
						color: Highcharts.getOptions().colors[ res[0]._color ],
						zIndex: res[0].zIndex,
						index: res[0].index,
					})
					jsondata.result.splice(jsondata.result.indexOf(res[0]), 1)
				}
				else if (res.length > 1) { }
				else { chart.series[i].remove() }
			}

			var s_len = jsondata.result.length;
			for (i = 0; i < s_len; i++) {
				var ser = chart.addSeries(jsondata.result[i]);
				ser.update({
					color: Highcharts.getOptions().colors[ jsondata.result[i]._color ],
					zIndex: jsondata.result[i].zIndex,
					index: jsondata.result[i].index,
				})
			}
			chart.redraw();
		});

		chart_time_subtitle(chart)
	}
	chart._reflow = function() {
		chart.reflow();
	}

	f();

	chart_time_subtitle(chart)

	// set up the updating of the chart each second
	setInterval(function() {f()}, update_period_ms);
}

// configure periodical update of the scatter+pie charts
function scatter_chart_updater(subpath, chart, chart_data_type) {
	var f = function() {
		$.getJSON(subpath+'json/'+chart_data_type+'/?callback=?', function(jsondata) {
			if (jsondata == null)
				return

			var s_len = jsondata.result.length;
			if (s_len == 0)
				return;

			var s_len = chart.series.length;
			for (_i = s_len; _i > 0; _i--) {
				var i = _i-1;
				var res = getObjects(jsondata.result, 'name', chart.series[i].name)

				if (res.length == 1) {
					chart.series[i].setData(res[0].data);
					chart.series[i].update({
						color: Highcharts.getOptions().colors[ res[0]._color ],
						zIndex: res[0].zIndex,
						index: res[0].index,
					})
					jsondata.result.splice(jsondata.result.indexOf(res[0]), 1)
				}
				else if (res.length > 1) { }
				else {
					if (chart.series[i].type == 'pie') {
						var res_pie = getObjects(jsondata.pie, 'name', chart.series[i].name)
						if (res_pie.length == 1) {
							chart.series[i].setData(res_pie[0].data)
							var d_len = res_pie[0].data.length
							for (j = 0; j < d_len; j++)
								chart.series[i].data[j].update({
									color: Highcharts.getOptions().colors[ res_pie[0].data[j]._color ]
								})
							jsondata.pie.splice(jsondata.pie.indexOf(res_pie[0]), 1)
						} else {
							chart.series[i].data = null
						}
					} else {
						chart.series[i].remove()
					}
				}
			}

			var s_len = jsondata.result.length;
			for (i = 0; i < s_len; i++) {
				var ser = chart.addSeries(jsondata.result[i]);
				ser.update({
					color: Highcharts.getOptions().colors[ jsondata.result[i]._color ],
					zIndex: jsondata.result[i].zIndex,
					index: jsondata.result[i].index,
				})
			}
			chart.redraw();
		});

		chart_time_subtitle(chart)
	}

	f();

	chart._reflow = function() {
		chart.reflow();
	}

	chart_time_subtitle(chart)

	// set up the updating of the chart each second
	setInterval(function() {f()}, update_period_ms);
}

// configure periodical update of the scatter+pie charts
function pie_chart_updater(subpath, chart, chart_data_type) {
	var f = function() {
		$.getJSON(subpath+'json/'+chart_data_type+'/?callback=?', function(jsondata) {
			if (jsondata == null)
				return

			var s_len = chart.series.length;
			for (_i = s_len; _i > 0; _i--) {
				var i = _i-1;
				var res_pie = getObjects(jsondata.pie, 'name', chart.series[i].name)
				if (res_pie.length == 1) {
					chart.series[i].setData(res_pie[0].data)
					var d_len = res_pie[0].data.length
					for (j = 0; j < d_len; j++)
						chart.series[i].data[j].update({
							color: Highcharts.getOptions().colors[ res_pie[0].data[j]._color ]
						})
					jsondata.pie.splice(jsondata.pie.indexOf(res_pie[0]), 1)
				} else {
					chart.series[i].data = null
				}
			}

			chart.redraw();
		});
		chart_time_subtitle(chart)
	}

	f();
	sub_pie_chart_updater(chart);

	chart._reflow = function() {
		chart.reflow();
		sub_pie_chart_updater(chart);
	}

	chart_time_subtitle(chart)

	// set up the updating of the chart each second
	setInterval(function() {f()}, update_period_ms);
}

function sub_pie_chart_updater(chart) {
	label1_x = 0.17
	label2_x = 0.50
	label3_x = 0.83

	label1_y = 0.08
	label2_y = 0.08
	label3_y = 0.08

	chart1_x = 0.17
	chart2_x = 0.50
	chart3_x = 0.83

	chart1_y = 0.28
	chart2_y = 0.28
	chart3_y = 0.28

	var element = document.getElementById(chart.renderTo.id);
	var style = element.currentStyle || window.getComputedStyle(element);
	width = parseFloat(style.width);
	height = parseFloat(style.height);

	if (height > width) {
		label1_x = 0.50
		label2_x = 0.50
		label3_x = 0.50

		label1_y = 0.10
		label2_y = 0.43
		label3_y = 0.76

		chart1_x = 0.50
		chart2_x = 0.50
		chart3_x = 0.50

		chart1_y = 0.17
		chart2_y = 0.50
		chart3_y = 0.83
	}

	render_label(chart, 'rl_tj', 'Total jobs', label1_x, label1_y)
	render_label(chart, 'rl_rj', 'Running jobs', label2_x, label2_y)
	render_label(chart, 'rl_qj', 'Queued jobs', label3_x, label3_y)

	sub_pie_pos(chart, chart.series[0], chart1_x, chart1_y);
	sub_pie_pos(chart, chart.series[1], chart2_x, chart2_y);
	sub_pie_pos(chart, chart.series[2], chart3_x, chart3_y);
// 	chart.series[0].update({
// 		center: [ chart.plotLeft + (0.17 * (chart.plotWidth-60)), '50%' ],
// 	});
// 	chart.series[1].update({
// 		center: [ chart.plotLeft + (0.50 * (chart.plotWidth-60)), '50%' ],
// 	});
// 	chart.series[2].update({
// 		center: [ chart.plotLeft + (0.83 * (chart.plotWidth-60)), '50%' ],
// 	});
}

function render_label(chart, label_id, text, center_x, center_y) {
	elem = document.getElementById(label_id)

	if (elem === null) {
		elem = chart.renderer.label(text, chart.plotLeft, 0, 'callout', 0, 0)
			.css({
				color: '#FFFFFF',
			}).attr({
				id: label_id,
				fill: 'rgba(0, 0, 0, 0.75)',
				padding: 8,
				r: 5,
				zIndex: 6,
			})
		elem.add();

		box = elem.getBBox();
		elem.attr({
			x: chart.plotLeft + (center_x * (chart.plotWidth-60)) - (0.5 * box.width) + 30,
			y: chart.plotTop + (center_y * chart.plotHeight) - (0.5 * box.height),
		})
	} else {
		var new_x = chart.plotLeft + (center_x * (chart.plotWidth-60)) - (0.5 * box.width) + 30;
		var new_y = chart.plotTop + (center_y * chart.plotHeight) - (0.5 * box.height);
		elem.setAttribute('transform', "translate\(" + new_x + "," + new_y + ")");
	}
}

function sub_pie_pos(chart, series, x, y) {
	series.update({
		center: [
			chart.plotLeft + (x * (chart.plotWidth-60)),
			chart.plotTop + (y * chart.plotHeight),
		],
	});
}

function chart_time_subtitle(chart) {
	var d = new Date();
	var now = "Last update: " + d.toLocaleTimeString()
	d.setMilliseconds(d.getMilliseconds() + update_period_ms)
	var later = "Next update: " + d.toLocaleTimeString()
	var subtitle = now + " | " + later

	chart.setTitle(null, { text : subtitle })
}

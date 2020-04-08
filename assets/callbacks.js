if (!window.dash_clientside) {
    window.dash_clientside = {}
}



window.dash_clientside.clientside3 = {
    update_table: function(clickdata, selecteddata, table_data, selectedrows, store) {
	/**
	 * Update selected rows in table when clicking or selecting in map
	 * chart
	 *
	 * Parameters
	 * ----------
	 *
	 * clickdata: object (dict)
	 *     clicked points
	 * selected: object (dict)
	 *     box-selected points
	 * table_data: list of dict
	 *     data of the table
	 * selectedrows: list of indices
	 *     list of selected countries to be updated
	 * store: list
	 *     store[1] is the list of countries to be used when initializing
	 *     the app
	 */
    	if ((!selecteddata) && (!clickdata)) {
	    // this is only visited when initializing the app
	    // we use a pre-defined list of indices
	    return store[1];
        }
	if (!selectedrows) {
	    selectedrows = [];
	}
	var ids = [...selectedrows];

	var countries = [];
	if (clickdata) {
	    var country = clickdata['points'][0]['customdata'][0];
	    countries.push(country);
	}
	if (selecteddata) {
	    var countries = [];
		for (i = 0; i < selecteddata['points'].length; i++) {
		    countries.push(selecteddata['points'][i]['customdata'][0]);
	    }
	}
	for (i = 0; i < countries.length; i++) {
	    for (j = 0; j < table_data.length; j++) {
		if (countries[i] == table_data[j]["country_region"]) {
		    if (selectedrows.includes(j)){
			var index = ids.indexOf(j);
			ids.splice(index, 1);
			}
		    else{
			ids.push(j);
		    }
		}
	    }
	}
	return ids;
    }
};

    
window.dash_clientside.clientside = {
    update_store_data: function(rows, selectedrows, cases_type, log_or_lin, store) {
	/**
	 * Update timeseries figure when selected countries change,
	 * or type of cases (active cases or fatalities)
	 *
	 * Parameters
	 * ----------
	 *
	 *  rows: list of dicts
	 *	data of the table
	 *  selectedrows: list of indices
	 *	indices of selected countries
	 *  cases_type: str
	 *	active or death
	 *  log_or_lin: str
	 *	log or linear axis
	 *  store: list
	 *	store[0]: plotly-figure-dict, containing all the traces (all
	 *	countries, data and prediction, for active cases and deaths)
	 *	store[1]: list of countries to be used at initialization
	 */
	var fig = store[0];
	if (!rows) {
           throw "Figure data not loaded, aborting update."
       }
	var new_fig = {};
	new_fig['data'] = [];
	new_fig['layout'] = fig['layout'];
	var countries = [];
	var max = 100;
	var max_data = 0;
	for (i = 0; i < selectedrows.length; i++) {
	    countries.push(rows[selectedrows[i]]["country_region"]);
	}
	if (cases_type === 'active'){
	    new_fig['layout']['annotations'][0]['visible'] = false;
	    new_fig['layout']['annotations'][1]['visible'] = true;
	    for (i = 0; i < fig['data'].length; i++) {
		var name = fig['data'][i]['name'];
		if (countries.includes(name) || countries.includes(name.substring(1))){
		    new_fig['data'].push(fig['data'][i]);
		    max_data = Math.max(...fig['data'][i]['y']);
		    if (max_data > max){
			max = max_data;
		    }
		}
	    }
	}
	else{
	    new_fig['layout']['annotations'][0]['visible'] = true;
	    new_fig['layout']['annotations'][1]['visible'] = false;
	    for (i = 0; i < fig['data'].length; i++) {
		var name = fig['data'][i]['name'];
		if (countries.includes(name.substring(2))){
		    new_fig['data'].push(fig['data'][i]);
		    max_data = Math.max(...fig['data'][i]['y']);
		    if (max_data > max){
			max = max_data;
		    }
		}
	    }
	}
	new_fig['layout']['yaxis']['type'] = log_or_lin;
	if (log_or_lin === 'log'){
	    new_fig['layout']['legend']['x'] = .65;
	    new_fig['layout']['legend']['y'] = .1;
	    new_fig['layout']['yaxis']['range'] = [1.2, Math.log10(max)];
	    new_fig['layout']['yaxis']['autorange'] = false;
	}
	else{
	    new_fig['layout']['legend']['x'] = .05;
	    new_fig['layout']['legend']['y'] = .8;
	    new_fig['layout']['yaxis']['autorange'] = true;
	}
        return new_fig;
    }
};


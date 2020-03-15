if (!window.dash_clientside) {
    window.dash_clientside = {}
}


window.dash_clientside.clientside2 = {
    get_store_data: function(data) {
        return data;
    }
};

window.dash_clientside.clientside3 = {
    update_table: function(clickdata, selecteddata, table_data, selectedrows) {
    	if ((!selecteddata) && (!clickdata)) {
           throw "Figure data not loaded, aborting update."
        }
	if (!selectedrows) {
	    selectedrows = [];
	}
	var ids = [...selectedrows];

	var countries = [];
	if (clickdata) {
	    var country = clickdata['points'][0]['customdata'][1];
	    countries.push(country);
	}
	if (selecteddata) {
	    var countries = [];
		for (i = 0; i < selecteddata['points'].length; i++) {
		    countries.push(selecteddata['points'][i]['customdata'][1]);
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
    update_store_data: function(selectedrows, rows, fig) {
	if (!rows) {
           throw "Figure data not loaded, aborting update."
       }
	var new_fig = {...fig};
	
	var countries = [];
	for (i = 0; i < rows.length; i++) {
	    countries.push(selectedrows[rows[i]]["country_region"]);
	}
	for (i = 0; i < new_fig['data'].length; i++) {
	    var name = new_fig['data'][i]['name'];
	    if (countries.includes(name) || countries.includes(name.substring(1))){
		new_fig['data'][i]['visible'] = true;
	    }
	    else{
		new_fig['data'][i]['visible'] = false;
	    }
	}
        return new_fig;
    }
};


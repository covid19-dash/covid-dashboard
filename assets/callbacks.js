if (!window.dash_clientside) {
    window.dash_clientside = {}
}


window.dash_clientside.clientside2 = {
    get_store_data: function(data) {
        return data;
    }
};

window.dash_clientside.clientside = {
    update_store_data: function(clickdata, selecteddata, selectedrows, rows, fig) {
	if ((!selecteddata) && (!clickdata) && (!rows)) {
           throw "Figure data not loaded, aborting update."
       }
	var new_fig = {...fig};
	
	if (selecteddata || rows) {
	    var countries = [];
	    if (selecteddata){
		for (i = 0; i < selecteddata['points'].length; i++) {
		    countries.push(selecteddata['points'][i]['customdata'][1]);
		}
	    }
	    if (rows){
		for (i = 0; i < rows.length; i++) {
		    countries.push(selectedrows[rows[i]]["country_region"]);
		}
	    }
	    for (i = 0; i < new_fig['data'].length; i++) {
		if (countries.includes(new_fig['data'][i]['name'])){
		    new_fig['data'][i]['visible'] = true;
		}
		
	    }
	}
	if (clickdata) {
	    var country = clickdata['points'][0]['customdata'][1];
	    for (i = 0; i < new_fig['data'].length; i++) {
		if (new_fig['data'][i]['name'] == country){
		    new_fig['data'][i]['visible'] = !(new_fig['data'][i]['visible']);
		}
	    }
	}
        return new_fig;
    }
};



if (!window.dash_clientside) {
    window.dash_clientside = {}
}


window.dash_clientside.clientside2 = {
    get_store_data: function(data) {
	console.log("hi");
	console.log(data);
        return data;
    }
};

window.dash_clientside.clientside = {
    update_store_data: function(clickdata, fig) {
	if (!clickdata) {
           throw "Figure data not loaded, aborting update."
       }
	console.log("hello");
	var new_fig = {...fig};
	var country = clickdata['points'][0]['customdata'][1];
	console.log(country);
	for (i = 0; i < new_fig['data'].length; i++) {
	    console.log(i);
            if (new_fig['data'][i]['name'] == country){
		new_fig['data'][i]['visible'] = true;
	    }
	}
	console.log(new_fig);
        return new_fig;
    }
};



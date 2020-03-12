
all:
	python3 app.py &
	sleep 8
	wget -r http://127.0.0.1:8050/ 
	wget -r http://127.0.0.1:8050/_dash-layout 
	wget -r http://127.0.0.1:8050/_dash-dependencies
	#wget http://127.0.0.1:8050/_dash-component-suites/dash_core_components/async-plotlyjs
	wget http://127.0.0.1:8050/_dash-component-suites/dash_core_components/async-graph.v1_8_1m1582838719.js
	sed -i 's/_dash-layout/_dash-layout.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js 
	sed -i 's/_dash-dependencies/_dash-dependencies.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js
	mv 127.0.0.1:8050/_dash-layout 127.0.0.1:8050/_dash-layout.json	
	mv 127.0.0.1:8050/_dash-dependencies 127.0.0.1:8050/_dash-dependencies.json
	mv 127.0.0.1:8050/assets/callback* 127.0.0.1:8050/assets/callbacks.js	
	# mv 127.0.0.1:8050/assets/style* 127.0.0.1:8050/assets/style.js
	mv 127.0.0.1:8050/assets/general-app-page* 127.0.0.1:8050/assets/general-app-page.css
	cp async* 127.0.0.1:8050/_dash-component-suites/dash_core_components/
	# ps | grep python | awk '{print $1}' | xargs kill -9	

clean:
	rm -r 127.0.0.1:8050/

teardown-python:
	ps | grep python | awk '{print $1}' | xargs kill -9

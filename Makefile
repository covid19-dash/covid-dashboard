
html:
	python3 app.py &
	sleep 20
	wget -r http://127.0.0.1:8050/ 
	wget -r http://127.0.0.1:8050/_dash-layout 
	wget -r http://127.0.0.1:8050/_dash-dependencies
	sed -i 's/_dash-layout/_dash-layout.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js 
	sed -i 's/_dash-dependencies/_dash-dependencies.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js
	mv 127.0.0.1:8050/_dash-layout 127.0.0.1:8050/_dash-layout.json	
	mv 127.0.0.1:8050/_dash-dependencies 127.0.0.1:8050/_dash-dependencies.json
	cp assets/* 127.0.0.1:8050/assets/
	cp _static/async* 127.0.0.1:8050/_dash-component-suites/dash_core_components/
	cp _static/async-table* 127.0.0.1:8050/_dash-component-suites/dash_table/
	ps | grep python | awk '{print $$1}' | xargs kill -9	

clean:
	rm -rf 127.0.0.1:8050/
	rm -rf joblib
	rm predictions.pkl

gh-pages:
	cd 127.0.0.1:8050 && touch .nojekyll && git init && git add * && git add .nojekyll && git commit -m "update" && git remote add origin https://github.com/covid19-dash/covid19-dash.github.io.git && git push -f origin master
	
all: gh-pages

teardown-python:
	ps | grep python | awk '{print $$1}' | xargs kill -9

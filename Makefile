
html:
	# First run our model
	# The following line matches a specific line in the python file
	# and truncate the file the. The goal is to avoid running the
	# last part of the notebook which takes very long to run
	sed '/# --------/,$$d' modeling.py > modeling_short.py
	sphx_glr_python_to_jupyter.py modeling_short.py
	jupyter nbconvert --execute --to html modeling_short.ipynb
	rm -rf modeling_short.ipynb modeling_short.py
	# Now build the app
	export DEBUG=False && python3 app.py &
	sleep 30
	wget -r http://127.0.0.1:8050/ 
	wget -r http://127.0.0.1:8050/_dash-layout 
	wget -r http://127.0.0.1:8050/_dash-dependencies
	sed -i 's/_dash-layout/_dash-layout.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js 
	sed -i 's/_dash-dependencies/_dash-dependencies.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js
	# Add our head
	sed -i '/<head>/ r head.html' 127.0.0.1:8050/index.html
	mv 127.0.0.1:8050/_dash-layout 127.0.0.1:8050/_dash-layout.json	
	mv 127.0.0.1:8050/_dash-dependencies 127.0.0.1:8050/_dash-dependencies.json
	cp modeling_short.html 127.0.0.1:8050/
	cp thumbnail.png 127.0.0.1:8050/
	cp assets/* 127.0.0.1:8050/assets/
	cp _static/async* 127.0.0.1:8050/_dash-component-suites/dash_core_components/
	cp _static/async-table* 127.0.0.1:8050/_dash-component-suites/dash_table/
	ps | grep python | awk '{print $$1}' | xargs kill -9	

update:
	cd COVID-19 && git pull

submodules:
	git submodule init
	git submodule update

clean:
	rm -rf 127.0.0.1:8050/
	rm -rf joblib
	rm -rf predictions.pkl
	rm -rf modeling_short.html

gh-pages:
	cd 127.0.0.1:8050 && touch .nojekyll && git init && git add * && git add .nojekyll && git commit -m "update" && git remote add origin https://github.com/covid19-dash/covid19-dash.github.io.git && git push -f origin master
	
all: gh-pages

teardown-python:
	ps | grep python | awk '{print $$1}' | xargs kill -9

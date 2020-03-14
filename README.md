# Raising awareness on COVID-19 evolution

The goal on this project is to raise awareness on the evolution of COVID.
The idea is to associate a visualization that shows data relevant to the
public with a didactic text on why such evolution is expected. A
forecasting model will be developed. 

# covid-dashboard

To launch the Dash app:

```
python3 app.py
```

then visit http://127.0.0.1:8050 with your browser

Deployed version https://covid-dash.herokuapp.com/

# Heroku deployment

git push heroku master
heroku ps:scale web=1

Visit  https://covid-dash.herokuapp.com

# Make static pages and deploy to github pages

See the `Makefile`.

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

Run
make

kill python process in terminal

cd 127.0.0.1:8050
python -m SimpleHTTPServer

GH Pages

touch .nojekyll
git init 
git add *
git add .nojekyll
git commit -m "update"
git remote add origin https://github.com/pydata-covid/pydata-covid.github.io.git
git push -f origin master

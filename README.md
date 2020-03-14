# Raising awareness on COVID-19 evolution

The goal on this project is to raise awareness on the evolution of COVID.
The idea is to associate a visualization that shows data relevant to the
public with a didactic text on why such evolution is expected. A
forecasting model will be developed. 

## Project vision

This web-based visualization (https://covid19-dash.github.io/) is meant
to help someone wanting to see or show what is a likely evolution of the
situation for his local environment. The utlimate goal is to influence
individual behavior, to decrease the spread.

So, the goal is to reach the general public, not experts familiar with
graphs and numbers.

To predictions and the associated text should be trustworthy, hence be
solid and sober, rather than fancy and dramatic. We would like this to be
approved by people with the relevant expertise.

# Development workflow

The application is built with a local dash app (https://plot.ly/dash/)
for development. Then a Makefile is used to turn this in a static
website.

## Local development

To launch the Dash app:

```
python3 app.py
```

then visit http://127.0.0.1:8050 with your browser

## Make static pages and deploy to github pages

See the `Makefile`.

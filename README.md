# Raising awareness on COVID-19 evolution

The goal on this project is to raise awareness on the evolution of COVID.
The idea is to associate a visualization that shows data relevant to the
public with a didactic text on why such evolution is expected. A
simple forecasting model estimates growth rates.

## Project vision

This web-based visualization (https://covid19-dash.github.io/) is meant
to help someone wanting to see or show what is a likely evolution of the
situation for their local environment. The ultimate goal is to influence
individual behavior, to decrease the spread.

The goal is to reach the general public, not experts familiar with graphs
and numbers. For this reason, effort is put on simplifying the
visualization and putting it along simple text.

The predictions and the associated text should be trustworthy, hence be
solid and sober, rather than fancy and dramatic.

## Well thougt-out visualization on COVID-19

COVID-19 is a serious issue and our visualization and data analysis needs
to be thought through serious. The following is a good read:
https://medium.com/nightingale/ten-considerations-before-you-create-another-chart-about-covid-19-27d3bd691be8

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

## Make static pages that will be deployed to github pages

The `Makefile` is used by github actions to deploy the model.

The Makefile
* runs the prediction engine on the latest data
* start the dash server
* persists it to a webpage that is not dependent on the server (local
  javascript callable)
* pushes to github pages

Care is taken to have a static page, to be able to handle the load with
many visits.

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
and numbers. For this reason, we put a lot of effort on simplifying the
visualization and putting it along simple text.

The predictions and the associated text should be trustworthy, hence be
solid and sober, rather than fancy and dramatic.

## Well thought-out visualization on COVID-19

COVID-19 is a serious issue and our visualization and data analysis needs
to be approached in a thoughtful, serious manner. The following would be a good read: <br>
https://medium.com/nightingale/ten-considerations-before-you-create-another-chart-about-covid-19-27d3bd691be8

# Development workflow

## Some details about the technologies

### Statistical modeling

The "modeling" notebook is generated from the "modeling.py" file, in the
Makefile. Only the first part of the notebook is executed in the
Makefile, stopping at "# -----".

The "modeling.py" can be run by itself in ipython, or edited in vscode,
atom, or with jupyter, that all support this mixed format.

### Web technologies

The application is built with a local Dash app (https://dash.plot.ly/)
for development. Then a Makefile is used to turn this in a static
website.

The Pure css grids (https://purecss.io/grids/) are used for layout, to
have a responsive design (ie that displays well on mobile phones).

## Local development

### Checkout the data

First, you need to checkout the upstream data (from Johns Hopkins), which
is contained in a git submodule. The easiest is to do:
```
make submodules
```


## Make static pages that will be deployed to github pages

The `Makefile` is used by github actions to deploy the model:
```
make html
```

The Makefile
* runs the prediction engine on the latest data
* start the dash server
* persists it to a webpage that is not dependent on the server (local
  javascript callable)
* pushes to github pages


Care is taken to have a static page, to be able to handle the load with
many visits.

An automatic schedule job is launched each day at 1:00 am (UTC) to build the
website and update with the latest available data.

## Interactive development

Launching locally the Dash app can be faster when working on the figures
or the CSS:

```
python3 app.py
```

then visit http://127.0.0.1:8050 with your browser

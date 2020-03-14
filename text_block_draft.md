# Documentation for covid-dashboard

The aim of this project is to provide measured predictions about the future of the COVID-19 epidemic.  Please keep in mind that predicting the future is hard, and there is a substantial amount of uncertainty around any predictions regarding this epidemic.

## Where do the data come from?
The data used here come from the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE), via their [Github page](https://github.com/CSSEGISandData/COVID-19). These data are aggregated from a large number of sources, described in more detail on their site.  The counts in the dataset describe the number of "confirmed cases", but note that these also include *presumptive positive* cases --- that is, cases that have the appearance of COVID-19 but have not been definitively confirmed by testing for the virus.

## What are the potential biases in the data?

With complex data from many different sources, there are many possible source of bias in the data.

### Reporting biases
Perhaps the greatest bias is that cases can only be counted if they seek out medical care. COVID-19 appears to cause mild or no symptoms in a sizeable proportion of people, which means that the reported counts underestimate the true total number of infected persons.  This could also cause biases between countries --- for example, if people are told to stay home unless their disease worsens, then fewer cases will be detected than if people are told to seek medical care for mild symptoms and receive testing for the virus.

### Test accuracy

A perfect diagnostic test would provide a positive result for every infected person, and a negative result for every non-infected person.  Unfortunately, it is almost impossible to create such a perfect test, so all diagnostic tests will result in some errors.  These can either be *false positive* errors (that is, saying that someone is infected when they are not), or a *false negative* error (saying that a person is not infected when they actually are). For example, the commonly used rapid tests for flu viruses have false negative rates of 30-70% and false positive rates of about 10%.  We don't yet know the error rates for the various testing methods in use for SARS-CoV-2, but we have already seen that the that test intially developed by the US Centers for Disease Control [had high rates of false positive results(https://www.propublica.org/article/cdc-coronavirus-covid-19-test).

### Population differences
There are differences between populations within and across countries that could affect the spread of the disease.  For example, the prevalence of chronic lung diseases (which increase the risk of severe COVID-19 infection) [vary between countries and between urban and rural enviornments](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4693508).  Differences in population density and in local customs (such as hand-shaking or face-kissing) could also affect the rates of disease transmission between different countries.

## How is the forecast made?


## How can you be sure that the forecast is accurate?






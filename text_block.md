# This is work in progress

Please come back later. We are quickly making progress.

# What do these data mean?

These visualizations give predictions about the future number of active COVID-19 cases. The predictions are based on extrapolating the growth observed in a given country over the last two weeks.

These predictions are only short-term extrapolation: predicting the future is hard, and epidemic dynamics will change with changes in public health measures, social interaction patterns, or even weather.  Please also keep in mind that each data point in these visualizations represents a person who has suffered or lost their life to this disease.

## Understanding exponential growth

In their early stages, outbreaks display *exponential growth*: the number of cases grows as a multiple of itself.  Let's say that Patient Zero infects two people, and then each of those infects two more people, and so on. The number of infected people will grow by a larger amount each day -- two on the first day, four on the second day, eight on the third day, and so on.  This is what we call exponential growth, because the number of cases on each day is some number raised to the power of the number of days. 

For a deeper explanation of how exponential growth relates to epidemics, see [this video](https://www.youtube.com/watch?v=Kas0tIxDvrg).

### The growth rate is not only a property of the virus

The local growth of an outbreaks is related to how likely one infected individual is to transmit the disease to another person. It is related to properties of the virus (such as how long it can stay on a surface), but also to how much people interact with each other, and public health measures such hand washing.

### Plotting in log scale

The plot of cases over time includes two different options: The linear plot shows the actual count of cases, while the log plot shows the *logarithm* of the number of cases - which is basically the number of times one has to multiply the number 10 in order to get the number of cases. This logarithm view has a direct relationship with the exponential growth of the epidemic: in such a view, an exponential growth appears as a straight line. You can think of the logarithm as the opposite of the exponential. 

In addition, the log plot lets us more easily see the relationships between trends over time when the actual numbers are very different.  Because the logarithm increasingly compresses large numbers, it makes it easier to see whether the rate of increase is similar between two countries, even when one has many more cases than the other. 


# Where do the data come from?

The data used here come from the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) [link](https://github.com/CSSEGISandData/COVID-19). These data are aggregated from a large number of sources, described in more detail on their site.  The counts in the dataset describe the number of "confirmed cases", but note that these also include *presumptive positive* cases --- that is, cases that have the appearance of COVID-19 but have not been definitively confirmed by testing for the virus.

# How is the forecast made?

We use the data from the last 14 days in each country to estimate the rate of growth for that country.  We then use that estimated rate of growth to project the future growth of cases in that country, assuming that it will continue to grow at the same rate exponentially. 

The thin dashed lines around the main line for each country reflect the degree of uncertainty in the model.   Note that major interventions (such as large scale social distancing and institutional closures) may reduce this growth rate (as you can see from the plots of cases in China); those factors are not currently included in the model.

Those who want to know more details about how the estimates are computed can find them [here](modeling_short.html).


## How can you be sure that the forecast is accurate?

We cannot. We are simply using the data to project further growth. However, you can see that the model has done well at predicting the growth rate over the last two weeks.  The model should be relatively accurate for the next few days, but becomes less accurate for farther-out days.


# What are the potential biases in the data?

Accurate measurements of health across populations are difficult. There are many sources of bias in the data.

## Reporting biases
Perhaps the greatest bias is that cases can only be counted if they seek out medical care or are tested. COVID-19 appears to cause mild or no symptoms in a sizeable proportion of people, which means that the reported counts underestimate the true total number of infected persons.  This could also cause biases between countries --- for example, if people are told to stay home unless their disease worsens, then fewer cases will be detected than if people are told to seek medical care for mild symptoms and receive testing for the virus. In addition, some countries test systematically many individuals, while other countries only test individuals with severe symptoms. This testing strategy, as well as well as the diagnostic criteria, may vary across time in a given country.

## Test accuracy

A perfect diagnostic test would provide a positive result for every infected person, and a negative result for every non-infected person.  Unfortunately, it is almost impossible to create such a perfect test, so all diagnostic tests will result in some errors.  These can either be *false positive* errors (that is, saying that someone is infected when they are not), or a *false negative* error (saying that a person is not infected when they actually are). For example, the commonly used rapid tests for flu viruses have false negative rates of 30-70% and false positive rates of about 10%.  We don't yet know the error rates for the various testing methods in use for SARS-CoV-2, but we have already seen that the that test intially developed by the US Centers for Disease Control [had high rates of false positive results](https://www.propublica.org/article/cdc-coronavirus-covid-19-test).

## Population differences
There are differences between populations within and across countries that could affect the spread of the disease.  For example, the prevalence of chronic lung diseases (which increase the risk of severe COVID-19 infection) [vary between countries and between urban and rural enviornments](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4693508).  Differences in population density and in local customs (such as hand-shaking or face-kissing greetings) could also affect the rates of disease transmission between different countries. In addition, the age distribution varies across countries, and as a consequence a larger fraction of the population is at risk in certain countries compared to others.


# What do these data mean?

The aim of these visualizations is to provide measured predictions about the future of the COVID-19 epidemic based on existing data.  Please keep in mind that predicting the future is hard, and there is a substantial amount of uncertainty around any predictions regarding this epidemic.  Please also keep in mind that each data point in these visualizations represents a person who lost their life to this disease.

## Where do the data come from?
The data used here come from the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE), via their [Github page](https://github.com/CSSEGISandData/COVID-19). These data are aggregated from a large number of sources, described in more detail on their site.  The counts in the dataset describe the number of "confirmed cases", but note that these also include *presumptive positive* cases --- that is, cases that have the appearance of COVID-19 but have not been definitively confirmed by testing for the virus.

## What are the potential biases in the data?

With complex data from many different sources, there are many possible source of bias in the data.

### Reporting biases
Perhaps the greatest bias is that cases can only be counted if they seek out medical care. COVID-19 appears to cause mild or no symptoms in a sizeable proportion of people, which means that the reported counts underestimate the true total number of infected persons.  This could also cause biases between countries --- for example, if people are told to stay home unless their disease worsens, then fewer cases will be detected than if people are told to seek medical care for mild symptoms and receive testing for the virus.

### Test accuracy

A perfect diagnostic test would provide a positive result for every infected person, and a negative result for every non-infected person.  Unfortunately, it is almost impossible to create such a perfect test, so all diagnostic tests will result in some errors.  These can either be *false positive* errors (that is, saying that someone is infected when they are not), or a *false negative* error (saying that a person is not infected when they actually are). For example, the commonly used rapid tests for flu viruses have false negative rates of 30-70% and false positive rates of about 10%.  We don't yet know the error rates for the various testing methods in use for SARS-CoV-2, but we have already seen that the that test intially developed by the US Centers for Disease Control [had high rates of false positive results](https://www.propublica.org/article/cdc-coronavirus-covid-19-test).

### Population differences
There are differences between populations within and across countries that could affect the spread of the disease.  For example, the prevalence of chronic lung diseases (which increase the risk of severe COVID-19 infection) [vary between countries and between urban and rural enviornments](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4693508).  Differences in population density and in local customs (such as hand-shaking or face-kissing) could also affect the rates of disease transmission between different countries.

## Understanding exponential growth and the log plot

The plot of cases over time includes two different options: The linear plot shows the actual count of cases, while the log plot shows the *logarithm* of the number of cases - which is basically the number of times one has to multiply the number 10 in order to get the number of cases. There are a couple of reasons that it's common to plot the logarithm of the data.

Most importantly, the logarithm has a direct relationship to the way in which epidemics can grow (at least in their early stages). You may be familiar with the idea of *exponential growth* -- this is the idea that the number of cases grows as a multiple of itself.  Let's say that Patient Zero infects two people, and then each of those infects two more people, and so on. The number of infected people will grow by a larger amount each day -- two on the first day, four on the second day, eight on the third day, and so on.  This is what we call exponential growth, because the number of cases on each day is some number raised to the power of the number of days.  You can think of the logarithm as the opposite of the exponential.  If we take a plot of perfect exponential growth and plot it using the logarithmic scale, it will look like a straight line.  

For a deeper explanation of how exponential growth relates to epidemics, see [this video](https://www.youtube.com/watch?v=Kas0tIxDvrg).

In addition, the log plot lets us more easily see the relationships between trends over time when the actual numbers are very different.  Because the logarithm increasingly compresses large numbers, it makes it easier to see whether the rate of increase is similar between two countries, even when one has many more cases. 


## How is the forecast made?


## How can you be sure that the forecast is accurate?






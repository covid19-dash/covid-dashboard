"""
Building the statistical model
"""

# %%
# Using joblib, to speed up interactions
from joblib import Memory
mem = Memory(location='.')

# %%
# Download the data
import data_input
data = mem.cache(data_input.get_data)()


# Below, we restrict ourselves to working only on the active cases
active = data['active']

# %%
# Plot the time course of the most affected countries
last_day = active.iloc[-1]
most_affected_countries = active.columns[last_day.argsort()][::-1]

import matplotlib.pyplot as plt
ax = active[most_affected_countries[:20]].plot(figsize=(7, 7))
ax.set_yscale('log')
ax.set_title("Log-scale plot of number of active cases")
plt.legend(loc='best', ncol=3)
plt.tight_layout()

# %%
# Some functions to build normalized smoothing kernels
import numpy as np

def ramp_kernel(start=14, middle=7):
    kernel = np.ones(start)
    kernel[:middle] = np.arange(middle) / float(middle)
    kernel /= kernel.sum()
    return kernel


def exp_kernel(start=14, growth=1.1):
    kernel = growth ** np.arange(start)
    kernel /= kernel.sum()
    return kernel

# %%
# The kernel that we use is determined via a historical replay: trying to
# predict the observation already seen from their past
kernel_size = 17
smoothing_kernel = exp_kernel(start=kernel_size, growth=1.6)

plt.figure()
plt.plot(smoothing_kernel)
plt.title('Our smoothing kernel')

# %%
# # A simple model: fit the last few points

# %%
# the log of the active counts in the last fortnight
last_fortnight = active.iloc[-kernel_size:]
log_last_fortnight = np.log(last_fortnight)
log_last_fortnight[log_last_fortnight == -np.inf] = 0

ax = log_last_fortnight[most_affected_countries[:20]].plot()
ax.set_title('Log of the number of active cases in the last fortnight')
plt.legend(loc='best', ncol=3)
plt.tight_layout()

# %%
# Our model-fitting routine: a weighted least square on the log of
# the active counts
import pandas as pd
import statsmodels.api as sm

def fit_on_window(data, kernel):
    """ Fit the last window of the data
    """
    kernel = smoothing_kernel
    data = active

    kernel_size = len(kernel)
    last_fortnight = data.iloc[-kernel_size:]
    log_last_fortnight = np.log(last_fortnight)
    log_last_fortnight[log_last_fortnight == -np.inf] = 0

    design = pd.DataFrame({'linear': np.arange(kernel_size),
                           'const': np.ones(kernel_size)})

    growth_rate = pd.DataFrame(data=np.zeros((1, len(data.columns))),
                               columns=data.columns)

    predicted_cases = pd.DataFrame()
    predicted_cases_lower = pd.DataFrame()
    predicted_cases_upper = pd.DataFrame()
    prediction_dates = pd.date_range(data.index[-kernel_size],
                                    periods=kernel_size + 7)

    for country in data.columns:
        mod_wls = sm.WLS(log_last_fortnight[country].values, design,
                         weights=kernel, hasconst=True)
        res_wls = mod_wls.fit()
        growth_rate[country] = np.exp(res_wls.params.linear)
        predicted_cases[country] = np.exp(res_wls.params.const +
                res_wls.params.linear * np.arange(len(prediction_dates))
            )
        # 1st and 3rd quartiles in the confidence intervals
        conf_int = res_wls.conf_int(alpha=.25)
        # We chose to account only for error in growth rate, and not in
        # baseline number of cases
        predicted_cases_lower[country] = np.exp(res_wls.params.const +
                conf_int[0].linear * np.arange(len(prediction_dates))
            )
        predicted_cases_upper[country] = np.exp(res_wls.params.const +
                conf_int[1].linear * np.arange(len(prediction_dates))
            )

    predicted_cases = pd.concat(dict(prediction=predicted_cases,
                                     lower_bound=predicted_cases_lower,
                                     upper_bound=predicted_cases_upper),
                                axis=1)
    predicted_cases['date'] = prediction_dates
    predicted_cases = predicted_cases.set_index('date')
    if kernel_size > 10:
        # Don't show predictions more than 10 days ago
        predicted_cases  = predicted_cases.iloc[kernel_size - 10:]

    return growth_rate, predicted_cases



# %%
# Fit it on the data
growth_rate, predicted_cases = fit_on_window(active, smoothing_kernel)

ax = growth_rate[most_affected_countries[:20]].T.plot(kind='barh',
    legend=False)
ax.set_title('Estimated growth rate')
plt.tight_layout()

print(growth_rate.T.sort_values(by=0))

# %%
# Plot our prediction

ax = last_fortnight[most_affected_countries[:10]].plot(figsize=(8, 7))
predicted_cases['prediction'][most_affected_countries[:10]].plot(
        ax=ax, style='--')
predicted_cases['lower_bound'][most_affected_countries[:10]].plot(
        ax=ax, style=':')
predicted_cases['upper_bound'][most_affected_countries[:10]].plot(
        ax=ax, style=':')

plt.legend(loc=(.8, -1.3))
ax.set_yscale('log')
ax.set_title('Number of active cases in the last fortnight and prediction')

# %%
# Save our results for the dashboard. We pickle a dict, because
# hierachical columns do not pickle right
import pickle
with open('predictions.pkl', 'wb') as out_file:
    pickle.dump(dict(prediction=predicted_cases['prediction'],
                     lower_bound=predicted_cases['lower_bound'],
                     upper_bound=predicted_cases['upper_bound'],
                    ),
                out_file)

# %%
# --------
# Now an analysis to optimize the kernel.
#
# This takes longer and is left out from the notebook displayed on the
# website (modeling_short)

# %%
# Historical replay to estimate an error

def historical_replay(data, kernel, threshold=50, prediction_horizon=4):
    """ Run the forecasting model in the past and measure how well it does.

    Parameters
    ==========
    data: dataframe
        The dataframe of the cases across countries (columns) and
        time (index)
    kernel: 1d numpy array
        The array of weights defining the window
    threshold: number
        Do not include a country in the evaluation if the
        last observed data point has less cases than "threshold"
    prediction_horizon: number
        The number of points we consider in the future to compute the
        error
    """

    all_errors = list()
    for i in range(len(kernel) + prediction_horizon, data.shape[0]):
        past_data = data[:i]
        # First, limit to countries with cases at the end that are more than
        # threshold
        past_data = past_data[past_data.columns[
                            (past_data.iloc[-prediction_horizon - 1:]
                            > threshold).all()]]
        train_data = past_data[:-prediction_horizon]
        test_data = past_data[-prediction_horizon:]
        _, predicted_data = fit_on_window(train_data, kernel)
        predicted_data = predicted_data['prediction']
        # We now compute the mean absolute relative error

        # Note that pandas' axis align magical matches the dates below
        relative_error = (test_data - predicted_data).dropna() / test_data
        relative_error = relative_error.abs().mean(axis=1)
        all_errors.append(relative_error.reset_index()[0])
    return np.mean(all_errors, axis=0)


# %%
# Calibrate the errors of our model for different kernels

# %%
# First with ramp kernels
errors_by_kernel = dict()

for start in range(8, 14):
    for middle in range(2, start + 1):
        kernel = ramp_kernel(start, middle)
        kernel_name = f'Ramp, from -{start} to -{middle}'
        errors = mem.cache(historical_replay)(active, kernel)
        errors_by_kernel[kernel_name] = (errors, start, middle)

# %%
# First we plot the errors are a function of prediction time
plt.figure()
for kernel_name, errors in errors_by_kernel.items():
    plt.plot(errors[0], label=kernel_name)
plt.legend(loc='best')
plt.xlabel('Days to predict')
plt.ylabel('Relative absolute error')
plt.title('Errors as a function of time')

# %%
# Our conclusion from the above is that the shape of the error does not
# depend much on the kernel

# %%
# We now plot the error after 4 days as a function of kernel params

plt.figure()
error, start, middle = zip(*errors_by_kernel.values())
plt.scatter(start, middle, np.array(error)[:, 1])
plt.scatter(start, middle, s=300*np.array(error)[:, 1],
            c=np.array(error)[:, 3], marker='o')
plt.colorbar()
plt.xlabel('start parameter')
plt.ylabel('middle parameter')
plt.title('Errors as a function of ramp kernel parameter')

# %%
# These results tell us that we want a ramp with a length of 10 and
# ramping all the way

# %%
# Now the exponential kernels
errors_by_kernel = dict()

for start in range(12, 18):
    for growth in [1.4, 1.5, 1.6, 1.7, 1.8, 1.9]:
        kernel = exp_kernel(start, growth)
        kernel_name = f'Exp, from -{start} with growth {growth}'
        errors = mem.cache(historical_replay)(active, kernel)
        errors_by_kernel[kernel_name] = (errors, start, growth)

# %%
# First we plot the errors are a function of prediction time
plt.figure()
for kernel_name, errors in errors_by_kernel.items():
    plt.plot(errors[0], label=kernel_name)
plt.legend(loc='best')
plt.xlabel('Days to predict')
plt.ylabel('Relative absolute error')
plt.title('Errors as a function of time')

# %%
# Our conclusion from the above is that the shape of the error does not
# depend much on the kernel

# %%
# We now plot the error after 4 days as a function of kernel params

plt.figure()
error, start, growth = zip(*errors_by_kernel.values())
plt.scatter(start, growth, np.array(error)[:, 1])
plt.scatter(start, growth, s=300*np.array(error)[:, 1],
            c=np.array(error)[:, 3], marker='o')
plt.colorbar()
plt.xlabel('start parameter')
plt.ylabel('growth parameter')
plt.title('Errors as a function of exp kernel parameter')

# %%
# We see that longer windows are better, with 1.6 growth.
#
# We chose not to explore longer than 17 days because these very long
# windows only improve prediction slightly, but risk biasing it when
# there is a change in public policy.

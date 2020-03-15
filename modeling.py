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
# Build a normalized smoothing kernel
import numpy as np
kernel_size = 14
smoothing_kernel = np.ones(kernel_size)
smoothing_kernel[:kernel_size // 2] = (np.arange(kernel_size // 2) /
                                        (kernel_size // 2))
smoothing_kernel /= smoothing_kernel.sum()

plt.figure()
plt.plot(smoothing_kernel)
plt.title('Our smoothing kernel')

# %%
# # A simpler model: fit the last few points

# %%
# the log of the active counts in the last fortnight
last_fortnight = active.iloc[-kernel_size:]
log_last_fortnight = np.log(last_fortnight)
log_last_fortnight[last_fortnight == -np.inf] = 0

ax = log_last_fortnight[most_affected_countries[:20]].plot()
ax.set_title('Log of the number of active cases in the last fortnight')
plt.legend(loc='best', ncol=3)
plt.tight_layout()

# %%
# We use a weighted least square on the log of the active counts
import pandas as pd
design = pd.DataFrame({'linear': np.arange(kernel_size),
                       'const': np.ones(kernel_size)})

import statsmodels.api as sm
growth_rate = pd.DataFrame(data=np.zeros((1, len(active.columns))),
                           columns=active.columns)

predicted_active_cases = pd.DataFrame()
prediction_dates = pd.date_range(active.index[-kernel_size],
                                 periods=kernel_size + 7)

for country in active.columns:
    mod_wls = sm.WLS(log_last_fortnight[country].values, design,
                    weights=smoothing_kernel, hasconst=True)
    res_wls = mod_wls.fit()
    growth_rate[country] = np.exp(res_wls.params.linear)
    predicted_active_cases[country] = np.exp(res_wls.params.const +
            res_wls.params.linear * np.arange(len(prediction_dates))
        )

ax = growth_rate[most_affected_countries[:20]].T.plot(kind='barh',
    legend=False)
ax.set_title('Estimated growth rate')
plt.tight_layout()

print(growth_rate.T.sort_values(by=0))

# %%
# Our prediction
predicted_active_cases['date'] = prediction_dates
predicted_active_cases = predicted_active_cases.set_index('date')

ax = predicted_active_cases[most_affected_countries[:10]].plot(
        style='--', figsize=(7, 7))

last_fortnight[most_affected_countries[:10]].plot(ax=ax)
plt.legend(loc='best', ncol=3)
ax.set_yscale('log')
ax.set_title('Number of active cases in the last fortnight and prediction')
plt.tight_layout()

# %%
# Save our results for the dashboard
predicted_active_cases.to_pickle('predictions.pkl')

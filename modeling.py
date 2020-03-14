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

data = data.fillna(value=0)

# %%
# Align columns and compute active cases
death, recovered = data['death'].align(data['recovered'], join='outer',
                                       fill_value=0)
inactive = death + recovered
confirmed, inactive = data['confirmed'].align(inactive, join='outer',
                                              fill_value=0)
active = confirmed - inactive

# Let's restrict ourselves to working only on the confirmed cases

# %%
# Plot the time course of the most affected countries
last_day = active.iloc[-1]
most_affected_countries = active.columns[last_day.argsort()][::-1]

ax = active[most_affected_countries[:20]].plot()
ax.set_yscale('log')
ax.set_title("Log-scale plot of number of cases")

# %%
# Plot the logarithmic derivative (relative increments)
#
# Model: intercept + exponential:
#          data = a + [1, b, b**2, b**3, ...]
# hence:   diff = data.diff() = [b, b**2, b**3, ...]
#          log = log(diff) = log(b) [1, 2, 3, ...]
#          diff(log) = [log(b) log(b) log(b)]
selected_countries = active.columns[last_day > 10]
selected_data = active[selected_countries]

import numpy as np
increments = selected_data.fillna(value=0).diff()
log_increments = np.log(increments)
# Ugly: set the relative increments to zero
log_increments[log_increments == -np.inf] = 0
relative_increments = log_increments.diff()
ax = relative_increments.plot()
ax.set_title("Daily relative increment")

# %%
# Build a normalized smoothing kernel
smoothing_kernel = np.ones(14)
smoothing_kernel[:7] = np.arange(7) / 7.
smoothing_kernel /= smoothing_kernel.sum()

import matplotlib.pyplot as plt
plt.figure()
plt.plot(smoothing_kernel)
plt.title('Our smoothing kernel')

# %%
# Temporal smoothing on our increments
smoothed_increments = relative_increments.copy()
smoothed_increments = smoothed_increments.fillna(value=0)
for country in selected_countries:
    smoothed_increments[country] = np.convolve(
        smoothed_increments[country], smoothing_kernel, mode='full')[
            1:-len(smoothing_kernel)+2]

ax = smoothed_increments.plot()
ax.set_title('Smoothed increments')

# %%
# Fit the intercept of an exponential model with the corresponding
# increment for the last few days of a country
last_increments = smoothed_increments.iloc[-1]
offsets = smoothed_increments.iloc[-1]
#predictions = np.


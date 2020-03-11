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

# Let's restrict ourselves to working only on the confirmed cases
data = data['confirmed']

# %%
# Plot the time course of the most affected countries
last_day = data.iloc[-1]
most_affected_countries = data.columns[last_day.argsort()][::-1]

ax = data[most_affected_countries[:20]].plot()
ax.set_yscale('log')

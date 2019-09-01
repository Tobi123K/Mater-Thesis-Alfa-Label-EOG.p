# Import libraries
import pandas as pd
import numpy as np

# Import matplot lib
%matplotlib inline

import matplotlib
import matplotlib.pyplot as plt

#
# Simulate data
#

# Get time values
t = np.arange(0,2*np.pi, 0.1)

# Amplitude is the sine function of time
a = np.sin(t)

# Plot sine function
plt.plot(t,a)

# Add horizontal line before and after the wave
y = np.zeros(10)
a = np.concatenate([y,a])
x = np.arange(-10,0,1)
t = np.concatenate([x,t])

plt.plot(t,a)

# Add horizontal line after wave
x = np.arange(2*np.pi,(2*np.pi+10),1)
t = np.concatenate([t,x])
a = np.concatenate([a,y])

plt.plot(t,a)

t_len = len(t)
mean = 0 # Average (mean) being zero
std = 0.01 # Standard deviation equals 1
noise = np.random.normal(mean, std, t_len)

# Add noise to signal
an = a + noise

plt.plot(t, an)

# 20 deg amplitude
# 10-100 ms
# 0-30 Hz

## y = [0, 1, 1, 1...]
# X = [[2, 3, 4, 5...], [0.2,  0.9, 1.9, 0...], [0.5, 0.7, 10, 10...]]  columns Amplitude, Acceleration, Velocity
# n = 4
# n = 4h /10

pd.DataFrame({'time':t,'amplitude':an}).to_csv('data.tsv',sep='\t', index=False)

# Load simulated data
table = pd.read_csv('data.tsv',sep='\t')

table.amplitude.plot()

def detect_states(signal, begin=0.5, end=-0.5):
    inside_wave = False # Assume it starts outside wave
    states = []
    for i in range(0, len(signal)):
        current_amplitude = signal[i]
        if current_amplitude > begin:
            inside_wave = True
        if current_amplitude < end:
            inside_wave = False
        # Save state
        states.append(inside_wave)
    return states


def count_durating_states(states, lower=10, upper=100):
    previous_state = states[0] # Initial state
    count = 0
    duration = 0
    for i in range(0, len(states)):
        current_state = states[i]
        if current_state != previous_state:
            previous_state = current_state
            if (duration > lower) & (duration < upper):
                count += 1
            duration = 0
        if current_state == True:
            duration += 1
    return count

# Detect states for two intervals
states_up = detect_states(table.amplitude, 0.5, 0)
states_down = detect_states(table.amplitude, 0, -0.5)

# Count waves for states defined on two intervals and sum them up
total = count_durating_states(states_up) + count_durating_states(states_down)
print(total)

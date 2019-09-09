# Import libraries
import pandas as pd
import numpy as np

# Import matplot lib
%matplotlib inline

import matplotlib
import matplotlib.pyplot as plt


#plt.plot(t, an)

# 20 deg amplitude
# 10-100 ms
# 0-30 Hz

## y = [0, 1, 1, 1...]
# X = [[2, 3, 4, 5...], [0.2,  0.9, 1.9, 0...], [0.5, 0.7, 10, 10...]]  columns Amplitude, Acceleration, Velocity
# n = 4
# n = 4h /10

#pd.DataFrame({'time':t,'amplitude':an}).to_csv('EOGdata3.tsv',sep='\t', index=False)

# Load simulated data
table = pd.read_csv('EOG02_blink.txt',sep='\t',names=['amplitude','amplitudeB']).reset_index().rename({'index':'time'},axis=1)

table.amplitude.plot()

def detect_states(signal, begin=0.2, end=0.1):
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


def count_durating_states(states, lower=10, upper=1000):
    previous_state = states[0] # Initial state
    count = 0
    duration = 0
    time = []
    for i in range(0, len(states)):
        current_state = states[i]
        if current_state != previous_state:
            previous_state = current_state
            if (duration > lower) & (duration < upper):
                count += 1
                time.append(duration)
            duration = 0
        if current_state == True:
            duration += 1
    return count, time

# Detect states for two intervals
states_up = detect_states(table.amplitude, 0.2, 0.1)
#states_down = detect_states(table.amplitude, 0, -0.5)

# Count waves for states defined on two intervals and sum them up
#total = count_durating_states(states_up) + count_durating_states(states_down)
#print(total)
n,time = count_durating_states(states_up, 10,1000)
print(n,time)


# Some imports
from __future__ import division
import serial, matplotlib.pyplot as plt, numpy as np, json

PIN = 'X2'
INTERVAL_US = 1000
NCOUNT = 100

# Scoped serial interface object
with serial.Serial('COM4', 9600, timeout=3) as ser:
    # Send the command to the "oscilloscope" to describe the data we want
    ser.write(PIN+','+str(INTERVAL_US)+','+str(NCOUNT)) # pin name, interval (us), number of measurements
    # Get the data from the "oscilloscope"
    line = ser.readline()   # read a '\n' terminated line

# Break up into two lists, one for time and another for voltage 
V = json.loads(line)
time_ms = 0.001*np.arange(0, len(V)*INTERVAL_US, INTERVAL_US)

# Plot them in Volts
plt.plot(time_ms, np.array(V)/4096*3.3, color = 'c', dashes = [2,2])

# Label the axes
plt.xlabel('time (ms)')
plt.ylabel('V (V)')

# Show the plot
plt.savefig('scopy.pdf')
plt.show()
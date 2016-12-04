# Import some uPython modules
import utime, pyb
from array import array

# Import classes from the pyb uPython library
from pyb import USB_VCP, ADC

from pyb import DAC
from pyb import LED
import math

# Turn on the light so you know something is happening
led = LED(4)
led.on()

# Write out a sinusoidal curve to channel X5, which is wired via a 
# female-female jumper to X2
# --
# create a buffer containing a sine-wave, using half-word samples
buf = array('H', 2048 + int(2047 * math.sin(2 * math.pi * i / 128)) for i in range(128))
dac = DAC(1, bits =12) # Wired to X5
dac.write_timed(buf, 400 * len(buf), mode=DAC.CIRCULAR)



# Instatiate the USB serial object
u = USB_VCP()

u.write('Hello world!!')

# Enter into an infinite loop
while True:
    
    # Get a line from the serial connection
    line = u.readline()
    
    # If there is nothing, line will be None
    if not line is None and line:
        
        # What you got is a byte object, convert from bytes (binary data) to python string
        line = line.decode('ascii')
        
        # Split the string at the delimiter, creating a 3-element list
        els = line.strip().split(',')
        # Get the scope parameters that are passed (0-based indexing!)
        pin = els[0]
        interval_us= int(els[1])
        count = int(els[2])
        
        # First extract the pin that we actually want to use as the enumerated value
        adc = ADC(getattr(pyb.Pin.board, pin))  # create an analog object from a pin name
        
        # Time right at the beginning
        ticks0_us = utime.ticks_us()
        # Time at the beginning
        tic_us = utime.ticks_us()
        # Output buffer for the data
        ostring = []
        # Iterate over the measurements
        for iel in range(count):
            # Set a flag saying we are going to still wait
            waiting = True
            while waiting:
                # Get the time now
                toc_us = utime.ticks_us()
                # If we are not ready to measure
                if toc_us - tic_us < interval_us:
                    # Keep waiting
                    waiting = True
                else:
                    # Ready to measure
                    # --------
                    # Do the measurement
                    val = adc.read()    # read an analog value in the range (0, 4096)
                    # Store the measurement
                    ostring.append(val)
                    # Reset the clock
                    tic_us = utime.ticks_us()
                    # Uncomment to see each measurement that is made
                    # u.write('got a measurement:'+str(val)+'\n')
                    waiting = False
        # Join the output elements into a comma delimited string
        u.write(str(ostring))
        del ostring
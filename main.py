# Import some uPython modules
import utime, pyb
# Import classes from the pyb uPython library
from pyb import USB_VCP, ADC

# Instatiate the USB serial object
u = USB_VCP()

# Enter into an infinite loop
while True:
    
    # Get a line from the serial connection
    line = u.readline()
    
    # If there is nothing, line will be None
    if line is not None:
        
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
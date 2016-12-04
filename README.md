# uscopy
A tiny repository showing how to interface pyboard with python master on PC

Guilty Parties
==============

Ian Bell and Duncan Bell, November 2016

Hardware
========

* PyBoard 1.1 running on a windows 7 PC on COM4

Installation
============

* Copy ``main.py`` over to PyBoard
* Run ``scopy.py`` on the master PC

Notes
=====

To get a list of serial ports once pyserial is installed, do:

    python -c "import serial.tools.list_ports; print [str(port) for port in serial.tools.list_ports.comports()]"

In this case X2 and X5 are jumpered together so that you can write the signal to pin X5 with DAC, and read data back in on pin X2
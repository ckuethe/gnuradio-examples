What's all this?
================

Random gnuradio things, so they don't stay trapped on my laptop forever

Doppler Sonar
-------------

A simple continuous wave doppler system using your computer's built-in speaker and microphone.

A basic FMCW sonar implementation has been added; still work in progress.

RF Loopback
-----------

Transmit tone from HackRF, receive on RTL-SDR. Just to make sure the TX and RX path works

XMLRPC Control
--------------

A simple demonstration of adding an XMLRPC endpoint to a flowgraph

Persistent Configuration
------------------------

This demonstrates how to save runtime variables and reload them at flowgraph start

Audio Waterfall
---------------

Porting @kpreid 's shinysdr audio waterfall to a grc flowgraph. Also
demonstrates the use of a signal generator to drive a VCO block to generate
the tuning control, and a python module block to import and run code more
or less verbatim from another source - https://github.com/kpreid/shinysdr/

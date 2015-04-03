#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Parameter Demo
# Author: Chris Kuethe <chris.kuethe@gmail.com>
# Generated: Fri Apr  3 10:46:01 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class parameter_demo(grc_wxgui.top_block_gui):

    def __init__(self, variable_frequency=4000, fixed_frequency=6000):
        grc_wxgui.top_block_gui.__init__(self, title="Parameter Demo")

        ##################################################
        # Parameters
        ##################################################
        self.variable_frequency = variable_frequency
        self.fixed_frequency = fixed_frequency

        ##################################################
        # Variables
        ##################################################
        self.slider_frequency = slider_frequency = variable_frequency
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        _slider_frequency_sizer = wx.BoxSizer(wx.VERTICAL)
        self._slider_frequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_slider_frequency_sizer,
        	value=self.slider_frequency,
        	callback=self.set_slider_frequency,
        	label='slider_frequency',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._slider_frequency_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_slider_frequency_sizer,
        	value=self.slider_frequency,
        	callback=self.set_slider_frequency,
        	minimum=-15000,
        	maximum=15000,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_slider_frequency_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, slider_frequency, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fixed_frequency, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.wxgui_fftsink2_0, 0))    


    def get_variable_frequency(self):
        return self.variable_frequency

    def set_variable_frequency(self, variable_frequency):
        self.variable_frequency = variable_frequency
        self.set_slider_frequency(self.variable_frequency)

    def get_fixed_frequency(self):
        return self.fixed_frequency

    def set_fixed_frequency(self, fixed_frequency):
        self.fixed_frequency = fixed_frequency
        self.analog_sig_source_x_0.set_frequency(self.fixed_frequency)

    def get_slider_frequency(self):
        return self.slider_frequency

    def set_slider_frequency(self, slider_frequency):
        self.slider_frequency = slider_frequency
        self._slider_frequency_slider.set_value(self.slider_frequency)
        self._slider_frequency_text_box.set_value(self.slider_frequency)
        self.analog_sig_source_x_1.set_frequency(self.slider_frequency)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-v", "--variable-frequency", dest="variable_frequency", type="intx", default=4000,
        help="Set variable_frequency [default=%default]")
    parser.add_option("-f", "--fixed-frequency", dest="fixed_frequency", type="intx", default=6000,
        help="Set fixed_frequency [default=%default]")
    (options, args) = parser.parse_args()
    tb = parameter_demo(variable_frequency=options.variable_frequency, fixed_frequency=options.fixed_frequency)
    tb.Start(True)
    tb.Wait()

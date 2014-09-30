#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: [FG]MRS Receiver
# Author: Chris Kuethe <chris.kuethe@gmail.com>
# Generated: Sun Sep 28 14:25:59 2014
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class fgmrs_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="[FG]MRS Receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.channel_width = channel_width = 25e3
        self.rf_freq_mhz = rf_freq_mhz = 462.5625
        self.decimation = decimation = int(samp_rate/channel_width)
        self.squelch = squelch = -20
        self.spec_size = spec_size = 480,256
        self.rf_freq = rf_freq = rf_freq_mhz*1.0e6
        self.decimated_rate = decimated_rate = samp_rate/decimation
        self.center_freq = center_freq = (int(rf_freq_mhz)+0.5)*1e6
        self.cctss_freq = cctss_freq = 0
        self.audio_rate = audio_rate = int(11025)

        ##################################################
        # Blocks
        ##################################################
        _squelch_sizer = wx.BoxSizer(wx.VERTICAL)
        self._squelch_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_squelch_sizer,
        	value=self.squelch,
        	callback=self.set_squelch,
        	label="Squelch (dBm)",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._squelch_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_squelch_sizer,
        	value=self.squelch,
        	callback=self.set_squelch,
        	minimum=-50,
        	maximum=0,
        	num_steps=50,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_squelch_sizer, 3, 3, 1, 2)
        self._cctss_freq_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.cctss_freq,
        	callback=self.set_cctss_freq,
        	label="Privacy Code",
        	choices=[0,67.0,71.9,74.4,77.0,79.7,82.5,85.4,88.5,91.5,94.8,97.4,100.0,103.5,107.2,110.9,114.8,118.8,123.0,127.3,131.8,136.5,141.3,146.2,151.4,156.7,162.2,167.9,173.8,179.9,186.2,192.8,203.5,210.7,218.1,225.7,233.7,241.8,250.3],
        	labels=['0 (Monitor)',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38],
        )
        self.GridAdd(self._cctss_freq_chooser, 3, 2, 1, 1)
        self.wxgui_waterfallsink2_1_0 = waterfallsink2.waterfall_sink_f(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=40,
        	ref_level=-25,
        	ref_scale=2.0,
        	sample_rate=audio_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Raw Audio Spectrum",
        	size=(spec_size),
        )
        self.GridAdd(self.wxgui_waterfallsink2_1_0.win, 2, 4, 1, 3)
        self.wxgui_waterfallsink2_1 = waterfallsink2.waterfall_sink_f(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=40,
        	ref_level=-25,
        	ref_scale=2.0,
        	sample_rate=audio_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Squelched Audio Spectrum",
        	size=(spec_size),
        )
        self.GridAdd(self.wxgui_waterfallsink2_1.win, 2, 1, 1, 3)
        self.wxgui_waterfallsink2_0_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=center_freq,
        	dynamic_range=40,
        	ref_level=-25,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="RF Spectrum",
        	size=(spec_size),
        )
        self.GridAdd(self.wxgui_waterfallsink2_0_0.win, 1, 1, 1, 3)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=40,
        	ref_level=-25,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Baseband Spectrum",
        	size=(spec_size),
        )
        self.GridAdd(self.wxgui_waterfallsink2_0.win, 1, 4, 1, 3)
        self._rf_freq_mhz_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.rf_freq_mhz,
        	callback=self.set_rf_freq_mhz,
        	label="Channel",
        	choices=[462.5625, 462.5875, 462.6125, 462.6375, 462.6625, 462.6875, 462.7125, 467.5625, 467.5875, 467.6125, 467.6375, 467.6625, 467.6875, 467.7125, 462.550, 462.575, 462.600, 462.625,462.650,462.675,462.700, 462.725],
        	labels=['FRS1 / GMRS 9',2,3,4,5,6,'FRS7 / GMRS15 ','FRS8',9,10,11,12,13,'FRS14','GMRS1',2,3,4,5,6,7,'GMRS8'],
        )
        self.GridAdd(self._rf_freq_mhz_chooser, 3, 1, 1, 1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(audio_rate),
                decimation=int(decimated_rate),
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(decimation, firdes.low_pass(
        	1, samp_rate, decimated_rate*0.8, decimated_rate*0.2, firdes.WIN_HAMMING, 6.76))
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(32, True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.audio_sink_0 = audio.sink(audio_rate, "", True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, rf_freq, 1, 0)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_ff(squelch, 0.0001, 1, False)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=audio_rate,
        	tau=75e-6,
        	max_dev=5e3,
        )
        self.analog_ctcss_squelch_ff_0 = analog.ctcss_squelch_ff(audio_rate, cctss_freq, 0.01, 0, 1, False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.wxgui_waterfallsink2_1_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.analog_ctcss_squelch_ff_0, 0))
        self.connect((self.analog_ctcss_squelch_ff_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.wxgui_waterfallsink2_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.wxgui_waterfallsink2_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_multiply_xx_0, 1))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_decimated_rate(self.samp_rate/self.decimation)
        self.set_decimation(int(self.samp_rate/self.channel_width))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.decimated_rate*0.8, self.decimated_rate*0.2, firdes.WIN_HAMMING, 6.76))
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0_0.set_sample_rate(self.samp_rate)

    def get_channel_width(self):
        return self.channel_width

    def set_channel_width(self, channel_width):
        self.channel_width = channel_width
        self.set_decimation(int(self.samp_rate/self.channel_width))

    def get_rf_freq_mhz(self):
        return self.rf_freq_mhz

    def set_rf_freq_mhz(self, rf_freq_mhz):
        self.rf_freq_mhz = rf_freq_mhz
        self.set_center_freq((int(self.rf_freq_mhz)+0.5)*1e6)
        self.set_rf_freq(self.rf_freq_mhz*1.0e6)
        self._rf_freq_mhz_chooser.set_value(self.rf_freq_mhz)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_decimated_rate(self.samp_rate/self.decimation)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch)
        self._squelch_slider.set_value(self.squelch)
        self._squelch_text_box.set_value(self.squelch)

    def get_spec_size(self):
        return self.spec_size

    def set_spec_size(self, spec_size):
        self.spec_size = spec_size

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.analog_sig_source_x_0.set_frequency(self.rf_freq)

    def get_decimated_rate(self):
        return self.decimated_rate

    def set_decimated_rate(self, decimated_rate):
        self.decimated_rate = decimated_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.decimated_rate*0.8, self.decimated_rate*0.2, firdes.WIN_HAMMING, 6.76))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.wxgui_waterfallsink2_0_0.set_baseband_freq(self.center_freq)

    def get_cctss_freq(self):
        return self.cctss_freq

    def set_cctss_freq(self, cctss_freq):
        self.cctss_freq = cctss_freq
        self._cctss_freq_chooser.set_value(self.cctss_freq)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.wxgui_waterfallsink2_1_0.set_sample_rate(self.audio_rate)
        self.wxgui_waterfallsink2_1.set_sample_rate(self.audio_rate)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = fgmrs_rx()
    tb.Start(True)
    tb.Wait()

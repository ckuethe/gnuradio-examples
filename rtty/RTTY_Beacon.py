#!/usr/bin/python
# Title    : RTTY_Beacon.py
# Function : RTTY FSK Beacon
# Author   : Pascal Schiks (C) 2008 gnu/gpl

from gnuradio import gr, blks2, usrp, audio
from gnuradio.wxgui import stdgui2, scopesink2
from math import pi

# Main Graph
class rtty_graph(stdgui2.std_top_block):

        # Constructor
	def __init__(self, frame, panel, vbox, argv):
		# Graphical part
		stdgui2.std_top_block.__init__(self, frame, panel, vbox, argv)

		# Config_____          
		tx_frequency = 14085000
 		usrp_interpolation = 400
		usrp_tx_rate = 128000000
		tx_side = 0
		tx_dev = 0
		audio_rate = 32000

		tx_subdev=(tx_side,tx_dev)
		usrp_tx_sample_rate = usrp_tx_rate / usrp_interpolation

		def rtty_gen_f(samplerate,speed,textdata):
			bitsamples=samplerate/speed
			mark = 900
			shift = 170
			space = mark+shift

			wavedata=[]

			letters = "_E\nA SIU\rDRJNFCKTZLWHYPQOBG_MXV_" 
			figures = "_3\n- '87\r_4_,!:(5+)2$6019?&_./;_"
			keyshift = 0

			for c in textdata:
				chartable = letters
				baudotdata=''
				shiftdata=''

				if((c >= '!') and  (c <='9')):
					if(not keyshift):
						shiftdata = '[MMSMM]'
                                        keyshift=1
				else:
					if(keyshift):
						shiftdata='[MMMMM]'
					keyshift=0	

				baudotdata = ']' + baudotdata
				if(keyshift):
					chartable = figures;
				baudotval=chartable.find(c)
                                for b in (16,8,4,2,1):
					if(baudotval>=b):
						baudotdata = 'M' + baudotdata
						baudotval = baudotval-b
					else:
						baudotdata = 'S' + baudotdata
                                baudotdata = shiftdata + '[' + baudotdata

				for bit in baudotdata:
 					if(bit == 'M'):
						bitval = mark
						bitlen = 1
 					if(bit == 'S'):
						bitval = space
						bitlen = 1
					if(bit == '['):
						bitval = space
						bitlen = 1
					if(bit == ']'):
						bitval = mark
						bitlen = 1.5

					for s in range(0,bitlen*bitsamples):
						wavedata.append(bitval)

			return gr.vector_source_f(wavedata, True)

		ryry = "RYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRYRY\r\n"
		callsign = "ZCZC DE PA3FKM PA3FKM -- RUNNING GNURADIO -- \r\n"
		fox = "+-- THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG --+\r\n "
		rttymsg = ryry+ryry+callsign+fox+"(0123456789)\r\n" 

		callgever = rtty_gen_f(audio_rate,45,rttymsg)

		lpf_coeffs = gr.firdes.low_pass(1,
                                                   audio_rate,
                                                   5000,
                                                   200)

                lpf = gr.fir_filter_fff (1, lpf_coeffs)

		fsk_f = gr.vco_f(audio_rate, 2*pi,0.5)

		fsk_c = gr.hilbert_fc(audio_rate/300)


		# IF low pass filter
                lpf_tx_coeffs  = gr.firdes.low_pass(32000,
                                                 audio_rate,
                                                 2000,
                                                 1000
                                                 )

                # Interpolation to usrp sample frequency
                fsk_resample = blks2.rational_resampler_ccc(
                                  usrp_tx_sample_rate / audio_rate,
				  1,
                                  taps=lpf_tx_coeffs
                               )


		usrp_tx = usrp.sink_c(0,usrp_interpolation)
                self.usrp_tx = usrp_tx

		speaker = audio.sink(audio_rate, "plughw:0,0");

		self.connect(callgever, lpf, fsk_f)
		self.connect(fsk_f, fsk_c, fsk_resample, usrp_tx)
		#self.connect(fsk_f, speaker)

		# Set Multiplexer
                mux = usrp.determine_tx_mux_value(usrp_tx,tx_subdev)
                usrp_tx.set_mux(mux)

		# Select subdevice
                usrp_tx_subdev = usrp.selected_subdev(usrp_tx,tx_subdev)

		# Tune subdevice                                               
                usrp_tx.tune(usrp_tx_subdev._which,usrp_tx_subdev, tx_frequency)

		# Enable Transmitter (Required if using one of the Flex boards) 
                usrp_tx_subdev.set_enable(True)

# Main caller program
if __name__ == '__main__':
	aplication = stdgui2.stdapp(rtty_graph,"RTTY generator")
	aplication.MainLoop()


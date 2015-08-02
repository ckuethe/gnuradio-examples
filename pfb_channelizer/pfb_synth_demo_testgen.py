#!/usr/bin/env python
# vim: tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab:
# -*- coding: utf-8 -*-
#
# Copyright 2015 Chris Kuethe <chris.kuethe@gmail.com>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import pymetar
import os
import dateutil.parser
import urllib2
from subprocess import Popen, PIPE

def windfix(wind):
	'''convert abbreviated compass directions to speakable text'''
	return ' '.join(map(lambda x: {'W': 'West', 'N':'North', 'E':'East', 'S':'South'}[x], wind))

def get_metar(station):
	'''fetch the METAR for a given station and return a pymetar object'''
	wx_fetcher = pymetar.ReportFetcher()
	dest = station + '.TXT'
	if not os.path.exists(dest): # pull from network
		raw_report = wx_fetcher.FetchReport(station)
		data = urllib2.urlopen(raw_report.reporturl).read()
		fd = open(dest, 'a+')
		fd.write(data)
		fd.close()
	else: # use local cache
		fd = open(dest)
		report_text = fd.read()
		fd.close()
		raw_report = wx_fetcher.MakeReport(station, report_text)

	wx_parser = pymetar.ReportParser()
	wx_report = wx_parser.ParseReport(raw_report)
	return wx_report

def compose_voice_message(wx_report):
	'''given a pymetar object, produce text to be fed to flite'''
	station = wx_report.getStationCity()
	report_time = dateutil.parser.parse(wx_report.getISOTime()).strftime("%A %B %d %Y at %H:%M UTC")
	wind = windfix(wx_report.getWindCompass())
	windspeed = wx_report.getWindSpeedMilesPerHour()
	c = wx_report.getConditions()

	txt  = ''
	txt += 'Here are the weather observations at %s \n' % station
	txt += 'for %s:\n' % report_time
	txt += 'The temperature is %d degrees,\n' % wx_report.getTemperatureFahrenheit()
	txt += 'winds from the %s at %d miles per hour.\n' % (wind, windspeed)
	txt += 'Relative humidity is %d%%\n' % wx_report.getHumidity()
	txt += 'Barometer is %.2f inches of mercury.\n' % (wx_report.getPressuremmHg() / 25.4)
	txt += 'Skies are %s with %s,\n' % (wx_report.getSkyConditions(), wx_report.getWeather())
	txt += 'Visibility %d miles\n' % wx_report.getVisibilityMiles()
	if c[0]:
		txt += 'Conditions include %s\n' % c[0]

	return txt

def main():
	'''given a list of weather stations, produce wav files of their observations'''

	airports = ['KJFK', 'KMIA', 'KSEA', 'KLAX', 'KDEN', 'PHNL', 'PANC']
	voice = ''
	channel_number = 0
	channel_width = 25e3
	nchan = len(airports)/2
	for icao in airports:
		voice = 'rms' if (voice == 'slt') else 'slt'
		wx_report = get_metar(icao)
		voice_message = compose_voice_message(wx_report)

		sign = "minus" if (channel_number < nchan) else "plus"
		freq = abs(channel_width * (channel_number - nchan) / 1000)
		prologue = "This is channel %d: base-band %s %d kilohertz.\n\n" % (channel_number, sign, freq)

		#print prologue
		#print voice_message
		args = ['flite', '-voice', voice, '/dev/stdin', "%d_%s_%s.wav" % (channel_number, icao, voice)]
		flite = Popen(args, stdin=PIPE)
		flite.stdin.write(prologue)
		flite.stdin.write(voice_message)
		flite.stdin.close()
		flite.wait()
		channel_number += 1

if __name__ == '__main__':
	'''It's not necessary to read the weather, but it's fun :) '''
	main()

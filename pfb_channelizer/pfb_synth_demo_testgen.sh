#!/bin/bash
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


# Just run this script and sample .wav files will be placed into $DEST
DEST="/tmp"

which flite > /dev/null
if [ $? -ne 0 ] ; then
	echo This script requires flite. Please install it and try again.
	exit 1
fi

CH=0 
SR=25000
NAMES="KJFK KMIA KSEA KLAX KDEN PHNL PANC" # same order as in the flowgraph...
NC=$(( $(echo $NAMES | wc -w) / 2 ))

for ICAO in $NAMES ; do
	if [ "x$VOICE" = "xslt" ] ; then
		VOICE="rms"
	else
		VOICE="slt"
	fi

	if [ $CH -lt $NC ] ; then
		SN="minus"
		X=-1
	else
		SN="plus"
		X=1
	fi
	FR=$(( $X * $SR * ( $CH - $NC ) / 1000 ))


	TMP=$(mktemp ${DEST}/flite.XXXXXXXXXX)
	OUTFILE="${DEST}/${CH}_${ICAO}_${VOICE}.wav"
	echo $OUTFILE
	ICAO=$(echo $ICAO | sed -re 's/(.)(.)(.)(.)/\1-\2-\3-\4/')
	printf 'This is channel %d.\nBase band %s %d kilohertz.\nFake weather report for: %s.\n' $CH $SN $FR $ICAO | \
		flite -voice $VOICE /dev/stdin $TMP
	mv $TMP $OUTFILE
	CH=$(( $CH + 1 ))
done

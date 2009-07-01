#!/bin/bash
# Fri Feb 16 11:39:35 CST 2007
# Dan Wanek <dwanek@nd.gov>
# #######################################################################################
#    This file is part of SVCstats.
#
#    SVCstats is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    SVCstats is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with SVCstats; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# #######################################################################################
# ============== Modify these for local settings ============== #
##########################################
BASE="${HOME}/SVCstats"
DATA="${BASE}/rrd/svc"
RRDTOOL="/usr/bin/rrdtool"
# ###### Per graph settings - should be cli args (someday) ######
# @ro @wo @rb @wb @re @we @rq @wq
DATUM="ro"
OUTF="${BASE}/img/svcstat_${DATUM}.png"
START=$(date -d "01/07/07 00:00" +%s)
END=$(date -d "01/31/07 23:59" +%s)
REGEX=".*.rrd"  # you can limit it down to mdisks if you want ".*mdisk[0-6].*"
##########################################
# ============================================================= #

rrdtool graph ${OUTF} -t "SVC - ${DATUM} stats" --start ${START} --end ${END} \
	$(
	index=0
	declare -a mdisks
	for node in `find ${DATA}/node{1,2} -regex "${REGEX}"`
	do
		mdisk=`basename ${node} .rrd`
		mdisk="${mdisk}_${index}"
		mdisks[$index]=$mdisk
		echo -n "DEF:${mdisk}=${node}:${DATUM}:AVERAGE "
		index=$((index+1))
	done
	mycdef=""
	index=0
	for def in ${mdisks[@]}
	do
		if [ $index -eq 0 ]
		then
			mycdef="mydata=$def"
		elif [ $index -lt 1 ]
		then
			mycdef="$mycdef,$def"
		else
			mycdef="$mycdef,$def,+"
		fi
		index=$((index+1))
	done
	echo -n "CDEF:$mycdef "
	) \
	LINE2:mydata#FF00FF

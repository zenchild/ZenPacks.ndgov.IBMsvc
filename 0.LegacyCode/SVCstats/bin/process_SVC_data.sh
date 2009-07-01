#!/bin/bash
# Wed, 03 Jan 2007 13:40:00 -0600
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
##########################################
declare -a nodeAR=( node1 node2 )
# ============================================================= #

IFS="
"

for node in ${nodeAR[@]}
do
	NODE_DATA=${DATA}/${node}
#for file in `find ${BASE}/xml/${node} -name "Nm_stats_*061112*" | sort`
for file in `find ${BASE}/xml/${node} -name "Nm_stats_*" | sort`
do
	echo "Parsing ${file} ..."
	DATE=`echo $(basename ${file} .xml) | cut -d_ -f4 | sed -e 's%\(..\)\(..\)\(..\)$%\2/\3/\1%'`
	TIME=`echo $(basename ${file} .xml) | cut -d_ -f5 | sed -e 's/\(..\)\(..\)\(..\)$/\1:\2:\3/'`
	STIME=$( date -d "${DATE} ${TIME}" +'%s' )

	for mdisk in `cat ${file} | grep '^<mdsk'`
	do
		MDISK="$(echo $mdisk | xml2 | sed -e 's/\/mdsk\/\@..=//g')"
		DATAFILE=${NODE_DATA}/md_$(echo $MDISK | cut -d\  -f1).rrd
		if [ ! -f ${DATAFILE} ]
		then
			echo "Creating RRD => ${DATAFILE}"
			${BASE}/lib/SVCcreate_rrd.sh ${DATAFILE} $((STIME-900))
		fi
		MDISK=$(echo $MDISK | sed -e 's/\s\+/:/g')

		#HEADER="ID $(echo $mdisk | xml2 | sed -e 's/\/mdsk\/\(@..\)=[^\s]\+/\1/g')"
		#ID @id @ro @wo @rb @wb @re @we @rq @wq
		#echo $HEADER

		#update @ro @wo @rb @wb @re @we @rq @wq
		${RRDTOOL} update ${DATAFILE} ${STIME}:$(echo ${MDISK} | cut -d: -f2,3,4,5,6,7,8,9 )
	done # for mdisk in ...

	if [ ! -d ${BASE}/xml/archive ]
	then
		mkdir ${BASE}/xml/archive
	fi
	mv ${file} ${BASE}/xml/archive
done # for file in ...
done # for node in ...

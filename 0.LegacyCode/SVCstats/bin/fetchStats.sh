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
NODE_IP="<primary SVC node IP>"
BASE_URL="http://${NODE_IP}/dumps/iostats"
NODE1="node1"  # Name of node 1
NODE2="node2"  # Name of node 2
##########################################
# ============================================================= #
cd ${BASE}

for file in `ssh -l admin ${NODE_IP} "svcinfo lsiostatsdumps -nohdr" | awk '{print $2}'`
do
	wget ${BASE_URL}/${file}
	#This removes a line in the XML that causes parsing problems
	cat ${file} | sed -f ${BASE}/lib/modify_xml.sed > ${BASE}/xml/${NODE1}/${file}.xml
	rm -f ${file}
done

ssh -l admin ${NODE_IP} "svctask cleardumps -prefix /dumps/iostats ${NODE1}"
ssh -l admin ${NODE_IP} "svctask cpdumps -prefix /dumps/iostats ${NODE2}"
ssh -l admin ${NODE_IP} "svctask cleardumps -prefix /dumps/iostats ${NODE2}"

for file in `ssh -l admin ${NODE_IP} "svcinfo lsiostatsdumps -nohdr" | awk '{print $2}'`
do
	wget ${BASE_URL}/${file}
	#This removes a line in the XML that causes parsing problems
	cat ${file} | sed -f ${BASE}/lib/modify_xml.sed > ${BASE}/xml/${NODE2}/${file}.xml
	rm -f ${file}
done

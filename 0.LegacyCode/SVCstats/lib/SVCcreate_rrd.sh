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


# Create a RRD that keeps an RRA Average for 365 days
STARTTIME=$2
# Variables @ro @wo @rb @wb @re @we @rq @wq
file=$1
rrdtool create ${file} --start ${STARTTIME} \
	--step 900 \
	DS:ro:COUNTER:1800:0:U \
	DS:wo:COUNTER:1800:0:U \
	DS:rb:COUNTER:1800:0:U \
	DS:wb:COUNTER:1800:0:U \
	DS:re:COUNTER:1800:0:U \
	DS:we:COUNTER:1800:0:U \
	DS:rq:COUNTER:1800:0:U \
	DS:wq:COUNTER:1800:0:U \
	RRA:AVERAGE:0.5:1:35040

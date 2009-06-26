#############################################################################
# Copyright © 2009 Dan Wanek <dwanek@nd.gov>
#
#
# This file is part of ZenPacks.ndgov.IBMsvc.
# 
# ZenPacks.ndgov.IBMsvc is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# ZenPacks.ndgov.IBMsvc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with ZenPacks.ndgov.IBMsvc.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################
__doc__ = """SVCclusterMap
Collects information related to a SVC cluster
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs


def parseCluster(results):
    """Parse the cluster output and make a dictionary out of it"""
    res = {}
    results = results.strip()
    for line in results.split('\n'):
        (key,val) = line.split('=')
        res[key] = val
    return(res)


class SVCclusterMap(CommandPlugin):
    """
    Run ztmp=`svcinfo lscluster -nohdr -delim :` &&
	svcinfo lscluster -bytes -delim = ${ztmp/:*/}'
    """
    command = r'ztmp=`svcinfo lscluster -nohdr -delim :` && svcinfo lscluster -bytes -delim = ${ztmp/:*/}'
    compname = ""
    modname = "ZenPacks.ndgov.IBMsvc.SVCcluster"


    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing lscluster for device %s" % device.id)
        res = parseCluster(results)
        om = self.objectMap()

	# For some reason the manufacturer does not carry through if there
	# are spaces in the osVersion string
	osVersion = re.sub(r'\s+', r'_', res['code_level'])
        om.setOSProductKey = MultiArgs(osVersion, "IBM")
        om.setHWProductKey = MultiArgs("2145","IBM") 
	om.snmpSysName = res['name']
        om.snmpDescr = "Cluster ID: %s" % (res['id'])
        return om


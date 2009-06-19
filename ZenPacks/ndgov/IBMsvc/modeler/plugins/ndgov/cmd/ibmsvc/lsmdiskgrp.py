__doc__ = """lsmdiskgrp
Collects information related to a SVC mdisk group.
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class lsmdiskgrp(CommandPlugin):
    """
    Run "svcinfo lsmdiskgrp -bytes -nohdr -delim :" to model mdisk group info.
    """
    command = 'svcinfo lsmdiskgrp -bytes -nohdr -delim :'
    relname = "mdiskgrp"
    modname = "ZenPacks.ndgov.IBMsvc.SVCmdiskgrp"

    def process(self, device, results, log):
	log.info('Results from command %s' % results)
        rm = self.relMap()
        results = results.strip()
	mdiskgrps = results.split("\n")
        bline = ""
        for mdg in mdiskgrps:
            om = self.objectMap()
            mdg = mdg.strip()
            mdg_a = mdg.split(':')
            om.id = self.prepId(mdg_a[0])
            #id:name:status:mdisk_count:vdisk_count:capacity:extent_size:free_capacity:virtual_capacity:used_capacity:real_capacity:overallocation:warning
            (om.mdiskgrp_name, om.status, om.mdisk_count, om.vdisk_count, om.capacity, om.free_capacity) = mdg_a[1],mdg_a[2],mdg_a[3],mdg_a[4],mdg_a[5],mdg_a[7]
            rm.append(om)
        return [rm]


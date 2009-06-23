__doc__ = """lsvdisk
Collects information related to a SVC vdisk
"""

import re
from pprint import pformat 
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class lsvdisk(CommandPlugin):
    """
    Run "svcinfo lsvdisk -bytes -nohdr -delim :" to model mdisk group info.
    """
    command = 'svcinfo lsvdisk -bytes -nohdr -delim :'
    compname = "mdiskgrp"
    relname = "vdisk"
    modname = "ZenPacks.ndgov.IBMsvc.SVCvdisk"

    def process(self, device, results, log):
	#log.info('Results from command %s' % results)
        rm = self.relMap()
        #rm = {}
        results = results.strip()
	vdisks = results.split("\n")
        bline = ""
        log.debug("=========================")
        log.debug("TYPE: %s" % type(rm))
        log.debug("MAPS: %s" % rm.maps)
        log.debug("COMPNAME: %s" % rm.compname )
        log.debug("Dev: %s" % dir(device) )
        log.debug("Dev Type: %s" % type(device) )
        log.debug("DevId: %s" % device.id )
        #log.debug("SELF: %s" % type(self) )
        log.debug("SELF DIR: %s" % dir(self) )
        log.debug("=========================")
        for vdisk in vdisks:
            om = self.objectMap()
            vdisk = vdisk.strip()
            vdisk_a = vdisk.split(':')
            om.id = self.prepId(vdisk_a[0])
            #if not rm.has_key(vdisk_a[5]):
            #   rm[vdisk_a[5]] = []

            #id:name:IO_group_id:IO_group_name:status:mdisk_grp_id:mdisk_grp_name:capacity:type:FC_id:FC_name:RC_id:RC_name:vdisk_UID:fc_map_count:copy_count:fast_write_state
            #log.debug("VDISK 1: %s" % vdisk_a[1] )
            #log.debug("VDISK 2: %s" % vdisk_a[2])
            #log.debug("VDISK 4: %s" % vdisk_a[4])
            #log.debug("VDISK 5: %s" % vdisk_a[5])
            #log.debug("VDISK 7: %s" % vdisk_a[7])
            #log.debug("VDISK 13: %s" % vdisk_a[13])
            (om.name, om.io_group_id, om.status, om.mdiskgrp_id, om.capacity, om.vdisk_UID) = vdisk_a[1],vdisk_a[2],vdisk_a[4],vdisk_a[5],vdisk_a[7],vdisk_a[13]
            #rm[vdisk_a[5]].append(om)
            rm.append(om)

 
        log.debug("RelMap:\n%s" % rm)
        #log.debug("First three modeled processes:\n%s" %
        #    pformat(rm.maps[:3])) 

        log.debug("=========================")
        return [rm]


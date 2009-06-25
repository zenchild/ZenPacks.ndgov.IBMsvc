__doc__ = """SVCcomponentMap Collects information related to a SVC mdisk group.
"""

import re from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

#def parseMdiskInfo(mdisk_a):
	"""
	Parse mDisk info out of command and return a hash like so:
	{'mdiskgrp_id' : { 'mdisk_id' : { .... mdisk info .... }}}
	----------------------------------------------------------
	*** svcinfo lsmdisk header fields ***
	0-4 = id:name:status:mode:mdisk_grp_id:
	5-9 = mdisk_grp_name:capacity:ctrl_LUN_#:controller_name:UID
	----------------------------------------------------------
	"""

def parseVdiskInfo(vdisk_a):
	"""
	Parse vDisk info out of command and return a hash like so:
	{'mdiskgrp_id' :
		{ 'vdisk1' : { .... vdisk info .... },
		  'vdisk2' : { .... vdisk info .... },
		  'vdiskn' : { .... vdisk info .... } }
	}
	----------------------------------------------------------
	*** svcinfo lsvdisk header fields ***
	0-4 =   id:name:IO_group_id:IO_group_name:status:
	5-9 =   mdisk_grp_id:mdisk_grp_name:capacity:type:FC_id:
	10-14 = FC_name:RC_id:RC_name:vdisk_UID:fc_map_count:
	15-16 = copy_count:fast_write_state
	----------------------------------------------------------
	"""
	vdisk_h = {}

	for vdisk in vdisk_a:
		vdata = vdisk.split(':')
		vdata_h = { 'name': vdata[1],
			'io_group_id': vdata[2],
			'status': vdata[4],
			'mdiskgrp_id': vdata[5],
			'vdisk_UID': vdata[13]}

		if not vdisk_h.has_key('vdata[5]'):
			vdisk_h[vdata[5]] = {}

		vdisk_h[vdata[5]][vdata[0]] = vdata_h
	
	return vdisk_h


class SVCcomponentMap(CommandPlugin):
	"""
	Run:
	svcinfo lsmdiskgrp -bytes -nohdr -delim :
		&& echo "__DELIM__"
		&& svcinfo lsvdisk -bytes -nohdr -delim :
		&& echo "__DELIM__"
		&& svcinfo lsmdisk -bytes -nohdr -delim :
	"""
	command = 'svcinfo lsmdiskgrp -bytes -nohdr -delim :' + \
		' && echo "__DELIM__"' + \
		' && svcinfo lsmdisk -bytes -nohdr -delim :' + \
		' && echo "__DELIM__"' + \
		' && svcinfo lsvdisk -bytes -nohdr -delim :'

	relname = "mdiskgrp"
	modname = "ZenPacks.ndgov.IBMsvc.SVCmdiskgrp"
	
	def process(self, device, results, log):
		log.info('Results from command %s' % results)
		rm = self.relMap()
		results = results.strip()
		(mdiskgrps,mdisks,vdisks) = results.split('__DELIM__')
		mdiskgrps = mdiskgrps.strip()
		mdiskgrps = mdiskgrps.split('\n')
		mdisks = mdisks.strip()
		mdisks = mdisks.split('\n')
		vdisks = vdisks.strip()
		vdisks = vdisks.split('\n')

		#mdisk_h = parseMdiskInfo(mdisks)
		vdisk_h = parseVdiskInfo(vdisks)

		for mdg in mdiskgrps:
			om = self.objectMap()
			mdg = mdg.strip()
			mdg_a = mdg.split(':')
			om.id = self.prepId(mdg_a[0])
			#id:name:status:mdisk_count:vdisk_count:capacity:extent_size:free_capacity:virtual_capacity:used_capacity:real_capacity:overallocation:warning
			(om.mdiskgrp_name, om.status, om.mdisk_count, om.vdisk_count, om.capacity,
					om.free_capacity)=mdg_a[1],mdg_a[2],mdg_a[3],mdg_a[4],mdg_a[5],mdg_a[7]
			om.modelVdisks = vdisk_h[om.id]
			rm.append(om)

		return [rm]

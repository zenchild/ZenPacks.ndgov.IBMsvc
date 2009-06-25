__doc__="""SVCmdiskgrp

IBM San Volume Controller(SVC) mDisk Group

$Id: $"""

__version__ = "1.0"

import locale

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import prepId

log = logging.getLogger("zen.SVCmdiskgrp")


class SVCmdiskgrp(DeviceComponent, ManagedEntity):
    """IBM San Volume Controller(SVC) mDisk Group"""

    portal_type = meta_type = 'SVCmdiskgrp'
    
    #**************Custom data Variables here from modeling************************
    
    mdiskgrp_name = ""
    status = ""
    mdisk_count = -1
    vdisk_count = -1
    free_capacity = -1
    capacity = -1
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'mdiskgrp_name', 'type':'string', 'mode':''},
        {'id':'status', 'type':'string', 'mode':''},
        {'id':'mdisk_count', 'type':'int', 'mode':''},
        {'id':'vdisk_count', 'type':'int', 'mode':''},
        {'id':'capacity', 'type':'int', 'mode':''},
        {'id':'free_capacity', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("cluster", ToOne(ToManyCont,
            'ZenPacks.ndgov.IBMsvc.SVCcluster', 'mdiskgrp')),
        ("vdisk", ToManyCont(ToOne,
            'ZenPacks.ndgov.IBMsvc.SVCvdisk', 'mdiskgrp')),
        )

    factory_type_information = ( 
        { 
            'id'             : 'SVCmdiskgrp',
            'meta_type'      : 'SVCmdiskgrp',
            'description'    : """SAN Volume Controller mDisk Group""",
            'icon'           : 'SanInterface_icon.gif',
            'product'        : 'ZenPacks.ndgov.IBMsvc',
            'factory'        : 'manage_addSVCmdiskgrp',
            'immediate_view' : 'viewSVCmdiskgrp',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSVCmdiskgrp'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW, )
                },
            )
          },
        ) 



	# ============= Special modeling methods ============= 

	"""
	These methods get automatically called if their name is
	a key in the ObjectMap created in the modeler plugin.
	Thank you to rocket's wonderful AIX-SNMP ZenPack for
	showing me the way.
	"""

	#def modelMdisks(self, mdisk_hash):
		"""
		This method creates SVCmdisk objects that are mapped
		to the correct mDiskgrp object.
		"""


	def modelVdisks(self, vdisk_hash):
        """
		This method creates SVCvdisk objects that are mapped
		to the correct mDiskgrp object.
        """
		for vdisk_id in vdisk_hash.keys():
			vdisk = manage_addvDisk(self.vdisk, vdisk_id)
			for vdisk_attr in vdisk_hash[vdisk_id]
				log.debug("vDisk Key: %s -> data: %s" %( vdisk_attr, vdisk_hash[vdisk_id][vdisk_attr]))
                attrib = getattr(vdisk, vdisk_attr)
                if callable( attrib ):
                    attrib(vdisk_hash[vdisk_id][vdisk_attr])
                else:
                    setattr(vdisk, vdisk_attr, vdisk_hash[vdisk_id][vdisk_attr])


	# =========== End Special modeling methods =========== 


    def device(self): return self.cluster()
    
    #THIS FUNCTION IS REQUIRED LEAVE IT BE IF NO RRD INFO IS PRESENT	    
    def getRRDNames(self):
		return ['']

    def getRRDTemplates(self):
        """
        """
        default = self.getRRDTemplateByName("SVC_mdiskgrp")
        if default:
            return [default]
        return []


InitializeClass(SVCmdiskgrp)

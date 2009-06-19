__doc__="""SVCvdisk

IBM San Volume Controller(SVC) vDisk

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


class SVCvdisk(DeviceComponent, ManagedEntity):
    """IBM San Volume Controller(SVC) vDisk"""

    portal_type = meta_type = 'SVCvdisk'
    
    #**************Custom data Variables here from modeling************************
    
    name = ""
    io_group_id = -1
    status = ""
    mdisk_grp_id = -1
    capacity = -1
    vdisk_UID = ""
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'name', 'type':'string', 'mode':''},
        {'id':'io_group_id', 'type':'int', 'mode':''},
        {'id':'status', 'type':'string', 'mode':''},
        {'id':'mdisk_grp_id', 'type':'int', 'mode':''},
        {'id':'capacity', 'type':'int', 'mode':''},
        {'id':'vdisk_UID', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("mdiskgrp", ToOne(ToManyCont,
            'ZenPacks.ndgov.IBMsvc.SVCmdiskgrp', 'vdisk')),
        )

    factory_type_information = ( 
        { 
            'id'             : 'SVCvdisk',
            'meta_type'      : 'SVCvdisk',
            'description'    : """SAN Volume Controller vDisk""",
            'icon'           : 'SanInterface_icon.gif',
            'product'        : 'ZenPacks.ndgov.IBMsvc',
            'factory'        : 'manage_addSVCvdisk',
            'immediate_view' : 'viewSVCvdisk',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSVCvdisk'
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



    #def viewName(self):
    #    return self.getPortName()
    #name = primarySortKey = viewName

    def device(self):
        return self.cluster()
    
    #def getPortName(self):
	#if str(self.Slot) == '-1':
	#    if str(self.Port) == '-1':
	#	return "Unknown"
	#return str(self.Slot) + "/" + str(self.Port)
    
    #def getLastChange(self):
	#if self.LastChange == 0:
	#    return "No Change"
	#else:
	#    days, remainder = divmod(self.LastChange,8640000)
	#    hours, remainder = divmod(remainder,360000)
	#    minutes, remainder = divmod(remainder,6000)
	#    seconds, remainder = divmod(remainder,100)
	#    return str(days) + " days " + str(hours) + ":" + str(minutes) + ":" + str(seconds)
    	
    #THIS FUNCTION IS REQUIRED LEAVE IT BE IF NO RRD INFO IS PRESENT	    
    def getRRDNames(self):
	return ['']


InitializeClass(SVCvdisk)

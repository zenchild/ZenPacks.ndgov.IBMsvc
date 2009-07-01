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
__doc__="""SVCiogrp

IBM San Volume Controller(SVC) IO Group

$Id: $"""

__version__ = "1.0"

import locale

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import prepId


class SVCiogrp(OSComponent, ManagedEntity):
    """IBM San Volume Controller(SVC) IO Group"""

    portal_type = meta_type = 'SVCiogrp'
    
    #**************Custom data Variables here from modeling************************
    
    iogrp_id = -1
    node_cnt = -1
    vdisk_cnt = -1
    host_cnt = -1
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'iogrp_id', 'type':'int', 'mode':''},
        {'id':'node_cnt', 'type':'int', 'mode':''},
        {'id':'vdisk_cnt', 'type':'int', 'mode':''},
        {'id':'host_cnt', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("cluster", ToOne(ToManyCont,
            'ZenPacks.ndgov.IBMsvc.SVCcluster', 'iogrp')),
        )

    factory_type_information = ( 
        { 
            'id'             : 'SVCiogrp',
            'meta_type'      : 'SVCiogrp',
            'description'    : """SAN Volume Controller IO Group""",
            'icon'           : 'SanInterface_icon.gif',
            'product'        : 'ZenPacks.ndgov.IBMsvc',
            'factory'        : 'manage_addSanInterface',
            'immediate_view' : 'viewSVCiogrp',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSVCiogrp'
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


InitializeClass(SVCiogrp)

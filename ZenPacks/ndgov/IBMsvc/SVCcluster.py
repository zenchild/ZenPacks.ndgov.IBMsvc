from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class SVCcluster(Device):
    """
	IBM San Volume Controller(SVC) Device
    """

    _relations = Device._relations + (
        ('iogrp', ToManyCont(ToOne,
            'ZenPacks.ndgov.IBMsvc.SVCiogrp', 'cluster')),
        ('mdiskgrp', ToManyCont(ToOne,
            'ZenPacks.ndgov.IBMsvc.SVCmdiskgrp', 'cluster')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'svcinfo'
            , 'name'            : 'SVC Info'
            , 'action'          : 'SVCclusterDetail'
            , 'permissions'     : (ZEN_VIEW, ) },
            )


    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(SVCcluster)

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
from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser

class lsvdisk(ComponentCommandParser):

    componentSplit = '\n'

    componentScanner = '^(?P<component>[^:]+)'

    scanners = [
        r'([^:]+):([^:]+):([^:]+):'
        r'([^:]+):([^:]+):([^:]+):'
        r'([^:]+):(?P<capacity>[^:]+):([^:]*):'
        r'([^:]*):([^:]*):([^:]*):'
        r'([^:]*):([^:]*):([^:]*):'
        r'([^:]*):([^:]*)'
        ]
    
    componentScanValue = 'id'


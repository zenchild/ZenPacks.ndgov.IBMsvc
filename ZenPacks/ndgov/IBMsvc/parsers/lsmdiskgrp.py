from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser

class lsmdiskgrp(ComponentCommandParser):

    componentSplit = '\n'

    componentScanner = '^(?P<component>[^:]+)'

    scanners = [
        r'([^:]+):([^:]+):([^:]+):'
        r'([^:]+):([^:]+):(?P<capacity>[^:]+):'
        r'([^:]+):(?P<free_capacity>[^:]+):([^:]+):'
        r'([^:]+):([^:]+):([^:]+):'
        r'([^:]+)'
        ]
    
    componentScanValue = 'id'


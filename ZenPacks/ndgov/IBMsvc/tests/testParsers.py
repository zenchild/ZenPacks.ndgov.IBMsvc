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
import os

from Products.ZenRRD.tests.BaseParsersTestCase import BaseParsersTestCase
from Products.ZenRRD.parsers.uptime import uptime

from ZenPacks.ndgov.IBMsvc.parsers.lsmdiskgrp import lsmdiskgrp


class SVCParsersTestCase(BaseParsersTestCase):

    def testSVCmdiskParsers(self):
        """
        Test the mDisk Group parser for the IBM SVC.
        """
        datadir = "%s/parserdata" % os.path.dirname(__file__)
        
        parserMap = {'svcinfo lsmdiskgrp -bytes -nohdr -delim :' : lsmdiskgrp } 

        self._testParsers(datadir, parserMap)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(SVCParsersTestCase))
    return suite


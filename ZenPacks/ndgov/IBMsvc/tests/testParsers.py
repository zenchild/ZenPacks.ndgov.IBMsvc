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


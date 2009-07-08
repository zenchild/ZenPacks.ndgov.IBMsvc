#!/usr/bin/env python
# coding=utf-8
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
__doc__ = """Monitor IBM SAN Volume Controllers

Continuously gathers and parses SVC performance data.
"""
import os
import time
import logging
log = logging.getLogger("zen.zensvc")

import Globals
from Products.ZenRRD.RRDDaemon import RRDDaemon
from Products.ZenRRD.RRDUtil import RRDUtil
from Products.ZenUtils.Driver import drive, driveLater


class ZenSVC(RRDDaemon):
	"""
	This class gathers and parses XML performance data from IBM SVC clusters.
	"""
	name = "zensvc"
	initialServices = RRDDaemon.initialServices + [
			'ZenPacks.ndgov.IBMsvc.services.ZenSVCConfig' ]
	configCycleInterval = 20
	#pingCycleInterval = 5*60

	def __init__(self):
		RRDDaemon.__init__(self, self.name)
		log.debug("********** Initializing ZenSVC")
		self.clusters = {}  #SVC clusters devId => devIP
		self.running = False
		self.statsPath = ""

	def connected(self):
		"""
		Twisted routine called when connected to zenhub, allowing
		us to begin initialization.
		"""
		def inner(driver):
			log.debug("***********Fetching ZenSVC Config")
			yield self.fetchConfig()
			driver.next()
			driveLater(self.configCycleInterval, inner)
		drive(inner).addCallbacks(self.collectPerfStats, self.errorStop)

	def fetchConfig(self):
		'Get configuration values from ZenHub'
		def inner(driver):
				yield self.model().callRemote('getDefaultRRDCreateCommand')
				createCommand = driver.next()
				yield self.model().callRemote('propertyItems')
				self.setPropertyItems(driver.next())
				#self.rrd = RRDUtil(createCommand, self.pingCycleInterval)
				yield self.model().callRemote('getThresholdClasses')
				self.remote_updateThresholdClasses(driver.next())
				yield self.model().callRemote('getCollectorThresholds')
				self.rrdStats.config(self.options.monitor,
										self.name,
										driver.next(),
										createCommand)
				""" While testing we'll use this to place the SVC Perf logs in"""
				if self.statsPath = "":
					yield self.model().callRemote('getStatsPath')
					self.statsPath = driver.next()
					log.debug("Got Path: %s" % self.statsPath)
					if not os.path.exists(self.statsPath):
						os.makedirs(self.statsPath)
				devices = []
				if self.options.device:
						devices = [self.options.device]
				yield self.model().callRemote('getDevices', devices)
				update = driver.next()
				if not isinstance(update, dict):
						log.error("********** getDevices returned: %r" % update)
				else:
						self.devices = update
		return drive(inner)

	def collectPerfStats(self, result=None):
		"""
		Do the actual collection and parsing of SVC iostats
		"""
		log.debug("*************** In collectPerfStats...")
		log.debug("***************************************")
		log.debug("Collecting for.... %s" % "\n".join(self.devices.values()))
		log.debug("***************************************")


if __name__ == '__main__':
	zensvc = ZenSVC()
	zensvc.run()

# Look at zencommand.py for hints and tips

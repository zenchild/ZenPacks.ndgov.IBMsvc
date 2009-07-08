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
from Products.ZenHub.services.PerformanceConfig import PerformanceConfig
import logging
log = logging.getLogger("zen.zensvc")
from ZenPacks.ndgov.IBMsvc.SVCcluster import SVCcluster

class ZenSVCConfig(PerformanceConfig):
	"""
	Service for fetching SVC Config data
	"""
	def getDeviceConfig(self, device):
		return (device.id, device.getManageIp())

	def remote_getStatsPath(self):
		packs = self.dmd.ZenPackManager.packs()
		statsPath="/tmp/statspath"
		for p in packs:
			if p.id == "ZenPacks.ndgov.IBMsvc":
				statsPath = p.path() + "/logs/svcstats"
				break
		return statsPath


	def remote_getDevices(self, devices):
		result = {}
		for d in self.config.getDevices():
			if isinstance(d, SVCcluster):
				result[d.id] = d.getManageIp()
		return result

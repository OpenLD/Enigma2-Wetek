#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##
##
## Copyright (c) 2012-2016 OpenLD
##          Javier Sayago <admin@lonasdigital.com>
## Contact: javilonas@esp-desarrolladores.com
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
##########################################################################
from enigma import *
from Screens.Screen import Screen
from Screens.Console import Console
from twisted.internet import threads
from Components.config import config
from Components.Button import Button
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.Harddisk import Harddisk
from Components.NimManager import nimmanager
from Components.About import about, getVersionString
from Components.Console import Console
from Components.Pixmap import MultiPixmap
from Components.Network import iNetwork
from Components.Language import language
from Components.Sources.StaticText import StaticText
from Components.PluginList import *
from Components.VariableText import VariableText
from Components.Element import cached
from Plugins.Plugin import PluginDescriptor
from Components.PluginComponent import plugins
from Tools.Directories import fileExists
from Tools.StbHardware import getFPVersion
from Tools.LoadPixmap import LoadPixmap
from ServiceReference import ServiceReference
from enigma import eLabel, iServiceInformation, eTimer, eConsoleAppContainer, getEnigmaVersionString, RT_HALIGN_LEFT, eListboxPythonMultiContent, gFont, getDesktop, eSize, ePoint
from boxbranding import getBoxType, getMachineBrand, getMachineName, getImageVersion, getImageBuild, getDriverDate
from time import *
from types import *
import sys, socket, commands, re, new, os, gettext, _enigma, enigma, subprocess, threading, traceback, time, datetime
from os import path, popen, system, listdir, remove as os_remove, rename as os_rename, getcwd, chdir

from re import search
from time import time

class LdsysInfo(Screen):
	skin = """
<screen name="LdsysInfo" position="70,35" size="1150,650">
<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LDteam/images/menu/fondo.png" alphatest="blend" transparent="1" />
<widget name="lab1" halign="left" position="15,10" size="660,650" font="Regular;20" scrollbarMode="showOnDemand">
</widget>
</screen>"""


	def __init__(self, session):
		Screen.__init__(self, session)
		self["lab1"] =  Label()

		self.onShow.append(self.updateInfo)

		self["myactions"] = ActionMap(["OkCancelActions"],
		{
			"ok": self.close,
			"cancel": self.close,
		}, -1)

	def updateInfo(self):
		rc = system("df -h > /tmp/syinfo.tmp")
		text = "BOX\n"
		f = open("/proc/stb/info/model",'r')
		text += "Model:\t" + about.getBoxType() + "\n"
 		f.close()
		#f = open("/proc/stb/info/chipset",'r')
 		#text += "Chipset:\t" + about.getChipSetString() + "\n"
		#f.close()
		cpuMHz = " - AMLogic AML-8726 MX (1,5 GHz) (Dual Core)"
		cmd = 'cat /proc/cpuinfo | grep "BogoMIPS" -m 1 | awk -F ": " ' + "'{print $2}'"
		try:
		    res = popen(cmd).read()
		except:
			res = ""
		bogoMIPS = ""
		if res:
			bogoMIPS = "" + res.replace("\n", "")
		gpuMHZ = "Mali MP400 (Dual Core)"
		f = open('/proc/cpuinfo', 'r')
		text += "CPU: \t" + about.getCPUString() + cpuMHz + "\n"
		#text += "CPU Load:\t%s" % str(about.getLoadCPUString()) + "\n"
		text += "BogoMIPS: \t" + bogoMIPS + "\n"
		text += "GPU: \t" + gpuMHZ + "\n"
		f.close()
		text += "\nMEMORY\n"
		memTotal = memFree = swapTotal = swapFree = 0
		for line in open("/proc/meminfo",'r'):
			parts = line.split(':')
			key = parts[0].strip()
			if key == "MemTotal":
				memTotal = parts[1].strip()
			elif key in ("MemFree", "Buffers", "Cached"):
				memFree += int(parts[1].strip().split(' ',1)[0])
			elif key == "SwapTotal":
				swapTotal = parts[1].strip()
			elif key == "SwapFree":
				swapFree = parts[1].strip()
		text += "Total memory:\t%s\n" % memTotal
		text += "Free memory:\t%s kB\n" % memFree
		text += "Memory Usage:\t%s" % str(about.getRAMusageString()) + "\n"
		text += "Swap total:\t%s \n" % swapTotal
		text += "Swap free:\t%s \n" % swapFree
		text += "\nSTORAGE\n"
		f = open("/tmp/syinfo.tmp",'r')
		line = f.readline()
		parts = line.split()
		text += parts[0] + "\t" + parts[1].strip() + "      " + parts[2].strip() + "    " + parts[3].strip() + "    " + parts[4] + "\n"
		line = f.readline()
		parts = line.split()
		text += "Flash" + "\t" + parts[1].strip() + "  " + parts[2].strip()  + "  " +  parts[3].strip()  + "  " +  parts[4] + "\n"
		for line in f.readlines():
			if line.find('/media/') != -1:
				line = line.replace('/media/', '   ')
				parts = line.split()
				if len(parts) == 6:
					text += parts[5] + "\t" + parts[1].strip() + "  " + parts[2].strip() + "  " + parts[3].strip() + "  " + parts[4] + "\n"
		f.close()
		os_remove("/tmp/syinfo.tmp")

		text += "\nSOFTWARE\n"
		f = open("/etc/ldversion",'r')
		text += "Firmware: \t" + f.readline() + "\n"
		f.close()
		text += "Version: \t" + about.getEnigmaVersionString() + "\n"
		text += "Kernel: \t" + about.getKernelVersionString() + "\n"

		self["lab1"].setText(text)

#!/usr/bin/python
# -*- coding: utf-8 -*-
# for localized messages
from . import _
from Screens.Screen import Screen
from Components.ActionMap import NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Sources.List import List
from Screens.ParentalControlSetup import ProtectedScreen
from Components.config import config
from Components.SystemInfo import SystemInfo


class VISIONMenu(Screen, ProtectedScreen):
	skin = """
		<screen name="VISIONMenu" position="center,center" size="610,410">
			<ePixmap pixmap="buttons/red.png" position="0,0" size="140,40" alphatest="on"/>
			<widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
			<widget source="menu" render="Listbox" position="15,60" size="330,290" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (2,2), size = (330,24), flags = RT_HALIGN_LEFT, text = 1), # index 0 is the MenuText,
						],
					"fonts": [gFont("Regular",22)],
					"itemHeight":25
					}
				</convert>
			</widget>
			<widget source="menu" render="Listbox" position="360,50" size="240,300" scrollbarMode="showNever" selectionDisabled="1">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (2,2), size = (240,300), flags = RT_HALIGN_CENTER|RT_VALIGN_CENTER|RT_WRAP, text = 2), # index 2 is the Description,
						],
					"fonts": [gFont("Regular",22)],
					"itemHeight":300
					}
				</convert>
			</widget>
			<widget source="status" render="Label" position="5,360" zPosition="10" size="600,50" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		</screen>"""

	def __init__(self, session, args=0):
		Screen.__init__(self, session)
		ProtectedScreen.__init__(self)
		self.setTitle(_("Vision Core"))
		self.menu = args
		self.list = []
		self["lab1"] = StaticText(_("OpenVision"))
		self["lab2"] = StaticText(_("Lets define enigma2 once more"))
		self["lab3"] = StaticText(_("Report problems to:"))
		self["lab4"] = StaticText(_("https://openvision.tech"))
		self["lab5"] = StaticText(_("Sources are available at:"))
		self["lab6"] = StaticText(_("https://github.com/OpenVisionE2"))
		if self.menu == 0:
			self.list.append(("Backup Manager", _("Backup Manager"), _("Manage settings backup."), None))
			self.list.append(("Image Manager", _("Image Manager"), _("Backup/Flash/ReBoot system image."), None))
			self.list.append(("Opkg Install", _("Opkg Install"), _("Install IPK's from your tmp folder."), None))
			self.list.append(("Mount Manager", _("Mount Manager"), _("Manage your devices mount points."), None))
			self.list.append(("Script Runner", _("Script Runner"), _("Run your shell scripts."), None))
			self.list.append(("Swap Manager", _("Swap Manager"), _("Create and Manage your SWAP files."), None))
			self.list.append(("Client Mode Box", _("Client Mode Box"), _("Use this box as a client of a server."), None))

			if SystemInfo["HasH9SD"]:
				self.list.append(("H9 SDcard Manager", _("H9 SDcard Manager"), _("Move Nand root to SD card"), None))
		self["menu"] = List(self.list)
		self["key_red"] = StaticText(_("Close"))

		self["shortcuts"] = NumberActionMap(["ShortcutActions", "WizardActions", "InfobarEPGActions", "MenuActions", "NumberActions"],
											{
											"ok": self.go,
											"back": self.close,
											"red": self.close,
											"menu": self.closeRecursive,
											"1": self.go,
											"2": self.go,
											"3": self.go,
											"4": self.go,
											"5": self.go,
											"6": self.go,
											"7": self.go,
											"8": self.go,
											"9": self.go,
											}, -1)
		self.onLayoutFinish.append(self.layoutFinished)
		self.onChangedEntry = []
		self["menu"].onSelectionChanged.append(self.selectionChanged)

	def isProtected(self):
		return config.ParentalControl.setuppinactive.value and config.ParentalControl.config_sections.visionmenu.value

	def createSummary(self):
		from Screens.PluginBrowser import PluginBrowserSummary

		return PluginBrowserSummary

	def selectionChanged(self):
		item = self["menu"].getCurrent()
		if item:
			name = item[1]
			desc = item[2]
		else:
			name = "-"
			desc = ""
		for cb in self.onChangedEntry:
			cb(name, desc)

	def layoutFinished(self):
		idx = 0
		self["menu"].index = idx

	def go(self, num=None):
		if num is not None:
			num -= 1
			if not num < self["menu"].count():
				return
			self["menu"].setIndex(num)
		current = self["menu"].getCurrent()
		if current:
			currentEntry = current[0]
			if self.menu == 0:
				if currentEntry == "Backup Manager":
					from BackupManager import VISIONBackupManager
					self.session.open(VISIONBackupManager)
				elif currentEntry == "Image Manager":
					from ImageManager import VISIONImageManager
					self.session.open(VISIONImageManager)
				elif currentEntry == "H9 SDcard Manager" and SystemInfo["HasH9SD"]:
					from H9SDmanager import H9SDmanager
					self.session.open(H9SDmanager)
				elif currentEntry == "Opkg Install":
					from IPKInstaller import VISIONIPKInstaller
					self.session.open(VISIONIPKInstaller)
				elif currentEntry == "Mount Manager":
					from MountManager import VISIONDevicesPanel
					self.session.open(VISIONDevicesPanel)
				elif currentEntry == "Script Runner":
					from ScriptRunner import VISIONScriptRunner
					self.session.open(VISIONScriptRunner, None)
				elif currentEntry == "Swap Manager":
					from SwapManager import VISIONSwap
					self.session.open(VISIONSwap)
				elif currentEntry == "Client Mode Box":
					from ClientModeBox import ClientModeBoxWizard
					self.session.open(ClientModeBoxWizard)

	def closeRecursive(self):
		self.close(True)

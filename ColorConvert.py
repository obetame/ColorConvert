#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sublime
import sublime_plugin
import re
from .utils import util
from .utils import colorName

matchRGBNumber = re.compile( r'\d{1,3}')

"""settings"""
convertMode = 'rgb'
capitalization = True

class ColorConvertCommand(sublime_plugin.TextCommand):
	# all value outputs
	outputs = []
	# view and edit
	view = None
	edit = None
	# if innerConvertMode != "", must convert to innerConvertMode
	innerConvertMode = convertMode

	def __init__(self, view):
		# Load settings
		self.view = view
		global convertMode
		global capitalization

		settings = sublime.load_settings("ColorConvert.sublime-settings")
		capitalization = settings.get("capitalization")
		settings.add_on_change("convertMode", loadSettings) # addEventListener for convertMode
		settings.add_on_change("capitalization", loadSettings) # addEventListener for capitalization

		loadSettings()

	# main
	def run(self, edit, value, isSelect):
		self.outputs = []
		self.edit = edit

		if (value != ""):
			self.innerConvertMode = value
		else:
			self.innerConvertMode = convertMode

		# select section entry
		if isSelect:
			self.selectModeReplace(self.view.sel())
		# all page(todo)
		else:
			self.allReplace()

	def handle(self, selectPart):
		# selectPart: '#1722DF' or 'rgba(0,0,0,1)' or 'hsla(100, 80.0%, 29.2%, 0.2)'...
		output = util.convertColor(selectPart, self.innerConvertMode) # core handle function

		if output != None:
			if capitalization:
				output = output.upper()
			self.outputs.append(output)

	"""replace view select color"""
	def selectModeReplace(self, regions):
		"""convert select section"""
		for region in regions:
			if not region.empty():
				self.handle(self.view.substr(region))

		for i, output in enumerate(self.outputs):
			for j, region in enumerate(regions):
				if i == j and not region.empty():
					self.view.replace(self.edit, region, output)

	"""replace view all color"""
	def allReplace(self):
		for name in ['rgb', 'rgba', 'hsl', 'hsla', 'hex', 'cmyk', 'hsv']:
			currentMatchRegion = self.view.find(util.matchRE.get(name), 0, sublime.IGNORECASE)
			allMatchRegin = self.view.find_all(util.matchRE.get(name), sublime.IGNORECASE)

			if name == self.innerConvertMode:
				continue

			for i in range(len(allMatchRegin)):
				if currentMatchRegion.empty():
					continue

				output = util.convertColor(self.view.substr(currentMatchRegion), self.innerConvertMode) # core handle function
				if output != None:
					self.view.replace(self.edit, currentMatchRegion, convertCase(output))

				currentMatchRegion = self.view.find(util.matchRE.get(name), currentMatchRegion.end(), sublime.IGNORECASE)

class ColorConvertNameToHexCommand(sublime_plugin.TextCommand):
	"""color name convert to hex
	"""

	def __init__(self, view):
		self.view = view

		# main
	def run(self, edit):
		self.edit = edit

		self.convertColorName()

	"""convert color name"""
	def convertColorName(self):
		regions = self.view.sel()
		outputs = []

		for region in regions:
			if not region.empty():
				name = colorName.mapColorName.get(self.view.substr(region).lower(), self.view.substr(region))
				output = colorName.colorName.get(name, name)

				if output != name:
					outputs.append(output)

		for i, output in enumerate(outputs):
			for j, region in enumerate(regions):
				if i == j and not region.empty():
					self.view.replace(self.edit, region, convertCase(output))

class ColorConvertHexToNameCommand(sublime_plugin.TextCommand):
	"""HEX convert To ColorName"""
	def __init__(self, view):
		self.view = view

	# main
	def run(self, edit):
		self.edit = edit

		self.covertColorName()

	def covertColorName(self):
		"""covert color name"""
		regions = self.view.sel()
		outputs = []
		hexsDict = colorName.getHexColorNameData()

		for region in regions:
			if not region.empty():
				hexName = util.handleHEXValueString(self.view.substr(region))

				if hexsDict.get(hexName):
					outputs.append(hexsDict.get(hexName))

		for i, output in enumerate(outputs):
			for j, region in enumerate(regions):
				if i == j and not region.empty():
					self.view.replace(self.edit, region, convertCase(output, True))

class ColorConvertAllHexToNameCommand(sublime_plugin.TextCommand):
	"""all HEX convert To ColorName"""
	def __init__(self, view):
		self.view = view

	# main
	def run(self, edit):
		self.edit = edit

		self.covertColorName()

	def covertColorName(self):
		"""covert color name"""
		currentMatchRegion = self.view.find(util.matchRE.get('hex'), 0, sublime.IGNORECASE)
		allMatchRegin = self.view.find_all(util.matchRE.get('hex'), sublime.IGNORECASE)
		hexsDict = colorName.getHexColorNameData()

		for i in range(len(allMatchRegin)):
			if currentMatchRegion.empty():
				continue

			select = util.handleHEXValueString(self.view.substr(currentMatchRegion))

			if select != None:
				hexName = hexsDict.get(select.upper()) 
				if hexName:
					self.view.replace(self.edit, currentMatchRegion, convertCase(hexName, True))

			currentMatchRegion = self.view.find(util.matchRE.get('hex'), currentMatchRegion.end(), sublime.IGNORECASE)

def convertCase(value, isColorName = False):
	"""Change case according to configuration
	
	Arguments:
		value {[str]} -- value data.
		isColorName {boolean} -- color name use Hump uppercase
	
	Returns:
		[str] -- Case value
	"""

	if capitalization:
		if isColorName:
			return colorName.mapColorName.get(value.lower())
		return value.upper()
	
	return value.lower()

def loadSettings():
	"""Loads settings from the ColorConvert.sublime-settings file"""

	global convertMode
	global capitalization

	settings = sublime.load_settings("ColorConvert.sublime-settings")

	convertMode = settings.get("convert_mode")
	capitalization = settings.get("capitalization")
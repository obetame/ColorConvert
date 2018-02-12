#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sublime
import sublime_plugin
import re
from .utils import util

matchRGBNumber = re.compile( r'\d{1,3}')

"""settings"""
covertModel = 'rgb'
capitalization = True

class ColorCovertCommand(sublime_plugin.TextCommand):
	# all value outputs
	outputs = []
	# view and edit
	view = None
	edit = None
	# if innerCovertModel != "", must covert to innerCovertModel
	innerCovertModel = covertModel

	def __init__(self, view):
		# Load settings
		self.view = view

		settings = sublime.load_settings("ColorCovert.sublime-settings")
		capitalization = settings.get("capitalization")
		settings.add_on_change("covertModel", loadSettings) # addEventListener for covertModel
		settings.add_on_change("capitalization", loadSettings) # addEventListener for capitalization

		loadSettings()

	# main
	def run(self, edit, value, isSelect):
		self.outputs = []
		self.edit = edit

		if (value != ""):
			self.innerCovertModel = value
		else:
			self.innerCovertModel = covertModel

		# select section entry
		if isSelect:
			self.selectModelReplace(self.view.sel())
		# all page(todo)
		else:
			self.allReplace()

	def handle(self, selectPart):
		# selectPart: '#1722DF' or 'rgba(0,0,0,1)' or 'hsla(100, 80.0%, 29.2%, 0.2)'...
		output = util.covertColor(selectPart, self.innerCovertModel) # core handle function

		if output != None:
			if capitalization:
				output = output.upper()
			self.outputs.append(output)

	"""replace view select color"""
	def selectModelReplace(self, regions):
		"""covert select section"""
		goodSelects = []
		for region in regions:
			if not region.empty():
				goodSelects.append(region)

		for region in goodSelects:
			self.handle(self.view.substr(region))

		for i, output in enumerate(self.outputs):
			for j, region in enumerate(regions):
				if i == j:
					self.view.replace(self.edit, region, output)

	"""replace view all color"""
	def allReplace(self):
		# firstMatchRegion = self.view.find(util.matchRE.get('hex'), 0, sublime.IGNORECASE)
		# print(firstMatchRegion.empty())
		for value in ['rgb', 'rgba', 'hsl', 'hsla', 'hex', 'cmyk', 'hsv']:
			firstMatchRegion = self.view.find(util.matchRE.get(value), 0, sublime.IGNORECASE)
			allMatchRegin = self.view.find_all(util.matchRE.get(value), sublime.IGNORECASE)

			for i in range(len(allMatchRegin)):
				if firstMatchRegion.empty():
					break

				output = util.covertColor(self.view.substr(firstMatchRegion), self.innerCovertModel) # core handle function
				if output != None:
					if capitalization:
						output = output.upper()
					self.view.replace(self.edit, firstMatchRegion, output)
				firstMatchRegion = self.view.find(util.matchRE.get('hex'), firstMatchRegion.begin(), sublime.IGNORECASE)

def loadSettings():
	"""Loads settings from the ColorCovert.sublime-settings file"""

	global covertModel
	global capitalization

	settings = sublime.load_settings("ColorCovert.sublime-settings")

	covertModel = settings.get("covert_model")
	capitalization = settings.get("capitalization")
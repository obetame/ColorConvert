#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sublime
import sublime_plugin
import re
from .utils import util

matchRGBNumber = re.compile( r'\d{1,3}')

"""settings"""
covertModel = 'rgb'

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
		settings.add_on_change("covertModel", loadSettings) # addEventListener for covertModel

		loadSettings()

	# main
	def run(self, edit, value, isSelect):
		self.outputs = []
		self.edit = edit
		selects = self.view.sel()

		if (value != ""):
			self.innerCovertModel = value

		# select section entry
		if isSelect:
			self.selectModelReplace(selects)
		# all page(todo)
		else:
			return

	def handle(self, selectPart):
		# selectPart: '#1722DF' or 'rgba(0,0,0,1)' or 'hsla(100, 80.0%, 29.2%, 0.2)'...
		output = util.covertColor(selectPart, self.innerCovertModel) # core handle function

		if output != None:
			self.outputs.append(output)

	def selectModelReplace(self, selects):
		"""covert select section"""
		if (len(selects) == 1 and selects[0].empty()):
			return

		for region in selects:
			self.handle(self.view.substr(region))

		for i, output in enumerate(self.outputs):
			for j, region in enumerate(selects):
				if i == j:
					self.view.replace(self.edit, region, output)

		self.innerCovertModel = covertModel # recover

# class ColorCovertModelCommand(sublime_plugin.TextCommand):
# 	# all value outputs
# 	outputs = []
# 	# view and edit
# 	view = None
# 	edit = None
# 	covertModel = None

# 	def run(self, edit, value, isSelect):
# 		covertModel = value
# 		self.outputs = []
# 		self.edit = edit
# 		selects = self.view.sel()

# 		if isSelect:
# 			print(value,isSelect)
# 		else:
# 			print(value,isSelect)

def loadSettings():
	"""Loads settings from the ColorCovert.sublime-settings file"""

	global covertModel

	settings = sublime.load_settings("ColorCovert.sublime-settings")

	covertModel = settings.get("covert_model")
	print("change model to:", covertModel)
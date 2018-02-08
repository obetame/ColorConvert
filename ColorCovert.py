#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sublime
import sublime_plugin
import re

mapHEX = {
	'A': 10,
	'B': 11,
	'C': 12,
	'D': 13,
	'E': 14,
	'F': 15,
	'1': 1,
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
	'0': 0
}

mapRGB = {
	0: '0',
	1: '1',
	2: '2',
	3: '3',
	4: '4',
	5: '5',
	6: '6',
	7: '7',
	8: '8',
	9: '9',
	10: 'A',
	11: 'B',
	12: 'C',
	13: 'D',
	14: 'E',
	15: 'F'
}

matchNumber = re.compile( r'\d{1,3}')

class ColorCovertCommand(sublime_plugin.TextCommand):
	# selected string '#1722DF'
	selectPart = ''
	# array model [1,7,2,2,D,F]
	needCovertPartArray = []
	# all value outputs
	outputs = []
	# view and edit
	view = ''
	edit = ''

	def init(self, region):
		self.selectPart = self.view.substr(region)

		if self.isHEX():
			self.HEX2RGB()
		else:
			self.RGB2HEX()

	# main
	def run(self, edit, value):
		self.outputs = []
		self.view = self.view
		self.edit = edit
		selects = self.view.sel()

		# normal entry
		if value == 'normal':
			if (len(selects) == 1 and selects[0].empty()):
				return

			for region in selects:
				self.init(region)

			loops = 0
			for output in self.outputs:
				loop = 0
				for region in selects:
					if loops == loop:
						self.view.replace(self.edit, region, output)
					loop += 1
				loops += 1
		# all page(todo)
		else:
			return

	def isHEX(self):
		if 'rgb' in self.selectPart:
			return False

		return True

	# handle HEX
	def handleHEXValue(self):
		value = self.selectPart.split("#")
		if len(value) <= 1:
			value = value[0]
		else:
			value = value[1]

		letters = []

		if (len(value) == 3):
			for letter in value:
				letters.append(letter.upper())
				letters.append(letter.upper())
		else:
			for letter in value:
				letters.append(letter.upper())

		self.needCovertPartArray = letters

	# HEX to RGB
	def HEX2RGB(self):
		self.handleHEXValue()

		rgb = ''
		for n in list(range(0, 5, 2)):
			valueArray = self.needCovertPartArray[n : n + 2]
			rgb += str(mapHEX[valueArray[0]] * 16 + mapHEX[valueArray[1]]) + ','

		self.outputs.append('rgb(' + rgb[:-1] + ')')

	# handle RGB
	def handleRGBValue(self):
		value = matchNumber.findall(self.selectPart)
		if len(value) <= 3: # rgb(0,0,0)
			self.needCovertPartArray = value
		else:								# rgb(0,0,0,1)
			self.needCovertPartArray = value[0:-1]

	# RGB to HEX
	def RGB2HEX(self):
		self.handleRGBValue()

		hex = '#'
		for n in list(range(0,3)):
			number = int(self.needCovertPartArray[n])
			if (number == 0):
				hex += '00'
				continue

			first = int(number / 16)
			secend = int(number % 16)
			hex += (mapRGB[first] + mapRGB[secend])

		self.outputs.append(hex)

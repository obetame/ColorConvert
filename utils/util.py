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

matchRGBNumber = re.compile( r'\d{1,3}')

def getSelectValueModel(selectPart):
	"""user select section value model"""
	if 'rgba' in selectPart:
		return 'rgba'
	elif 'rgb' in selectPart:
		return 'rgb'
	elif 'hsla' in selectPart:
		return 'hsla'
	elif 'hsl' in selectPart:
		return 'hsl'
	else:
		return 'hex'

# handle HEX
def handleHEXValue(selectPart):
	value = selectPart.split("#")
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

	return letters

# HEX to RGB
def HEX2RGB(selectPart):
	lettersArray = handleHEXValue(selectPart)

	rgb = ''
	for n in list(range(0, 5, 2)):
		valueArray = lettersArray[n : n + 2]
		rgb += str(mapHEX[valueArray[0]] * 16 + mapHEX[valueArray[1]]) + ','

	return 'rgb(' + rgb[:-1] + ')'

# handle RGB
def handleRGBValue(selectPart):
	value = matchRGBNumber.findall(selectPart)
	if len(value) <= 3: # rgb(0,0,0)
		return value
	else:								# rgb(0,0,0,1)
		return value[0:-1]

# RGB to HEX
def RGB2HEX(selectPart):
	numberArray = handleRGBValue(selectPart)

	hex = '#'
	for n in list(range(0,3)):
		number = int(numberArray[n])
		if (number == 0):
			hex += '00'
			continue

		first = int(number / 16)
		secend = int(number % 16)
		hex += (mapRGB[first] + mapRGB[secend])

	return hex

# RGB to HSL
def RGB2HSL(selectPart):
	numberArray = handleRGBValue(selectPart)

	hex = '#'
	for n in list(range(0,3)):
		number = int(numberArray[n])
		if (number == 0):
			hex += '00'
			continue

		first = int(number / 16)
		secend = int(number % 16)
		hex += (mapRGB[first] + mapRGB[secend])

	return hex

# RGB to RGBA
def RGB2RGBA(selectPart):
	value = selectPart[:-1] + ",1)"
	return value.replace("rgb", "rgba")

# RGBA to RGB
def RGBA2RGB(selectPart):
	valueArray = selectPart.split(",")
	valueArray[3] = ")"

	return ",".join(valueArray).replace("rgba", "rgb")[:-2] + ")"

switcher = {
	"rgb": {
		"rgb": lambda value: value,
		"rgba": RGB2RGBA,
		"hex": RGB2HEX
	},
	"rgba": {
		"rgb": RGBA2RGB,
		"rgba": lambda value: value
	},
}

def covertColor(selectPart, covertModel):
	"""value(selectPart) covert to need model(covertModel)"""
	valueModel = getSelectValueModel(selectPart)
	handleObj = switcher.get(valueModel, {})
	handleFun = handleObj.get(covertModel, lambda: None)

	return handleFun(selectPart)
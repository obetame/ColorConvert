#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

matchRGBHSLNumber = re.compile( r'\d*\.*\d{1,3}\%*')

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

# handle RGB
def handleRGBValue(selectPart):
	value = matchRGBHSLNumber.findall(selectPart)

	newValue = []
	"""handle number is '.5' a class """
	for v in value:
		if v[0] == ".":
			newValue.append(float("0." + v[1:]))
		elif "%" in v:
			number = float(v.split("%")[0]) # 89% -> 89
			newValue.append(number / 100)
		else:
			newValue.append(float(v) / 255)
	return newValue

# handle HSL
def handleHSLValue(selectPart):
	value = matchRGBHSLNumber.findall(selectPart)

	newValue = []
	"""handle number is '.5' a class """
	for v in value:
		if v[0] == ".":
			newValue.append(float("0." + v[1:]))
		elif "%" in v:
			newValue.append(int(v.split("%")[0]))
		else:
			newValue.append(int(v))
	return newValue

# HEX to RGB
def HEX2RGB(selectPart, isAlpha = False, alpha = 1):
	lettersArray = handleHEXValue(selectPart)

	rgb = ''
	for n in list(range(0, 5, 2)):
		valueArray = lettersArray[n : n + 2]
		rgb += str(mapHEX[valueArray[0]] * 16 + mapHEX[valueArray[1]]) + ','

	if isAlpha:
		return 'rgba(' + rgb[:-1] + "," + alpha + ')'
	else:
		return 'rgb(' + rgb[:-1] + ')'

# RGB to HEX
def RGB2HEX(selectPart):
	numberArray = handleRGBValue(selectPart)

	valueArray = []
	for value in numberArray:
		valueArray.append(value * 255)

	hex = '#'
	for n in list(range(0,3)):
		number = valueArray[n]
		if (number == 0):
			hex += '00'
			continue

		first = int(number / 16)
		secend = int(number % 16)
		hex += (mapRGB[first] + mapRGB[secend])

	return hex

# RGB to RGBA
def RGB_HSL2RGBA_HSLA(selectPart, input, output):
	value = selectPart[:-1] + ",1)"
	return value.replace(input, output)

# RGBA to RGB
def RGBA_HSLA2RGB_HSL(selectPart, input, output):
	valueArray = selectPart.split(",")
	valueArray[3] = ")"

	return ",".join(valueArray).replace(input, output)[:-2] + ")"

# RGB to HSL
def RGB2HSL(selectPart, isAlpha = False, alpha = 1):
	numberArray = handleRGBValue(selectPart)
	maxN = max(numberArray)
	minN = min(numberArray)
	h = ""
	s = ""
	l = (maxN + minN) / 2

	if maxN == minN:
		h = s = 0
	else:
		mid = maxN - minN
		if l > 0.5:
			s = mid / (2 - maxN - minN)
		elif l <= 0.5 and l > 0:
			s = mid / (maxN + minN)
		elif l == 0:
			s = 0

		if maxN == numberArray[0] and numberArray[1] >= numberArray[2]:
			h = 60 * (numberArray[1] - numberArray[2]) / mid + 0
		elif maxN == numberArray[0] and numberArray[1] < numberArray[2]:
			h = 60 * (numberArray[1] - numberArray[2]) / mid + 360
		elif maxN == numberArray[1]:
			h = 60 * (numberArray[2] - numberArray[0]) / mid + 120
		elif maxN == numberArray[2]:
			h = 60 * (numberArray[2] - numberArray[0]) / mid + 120

	if isAlpha:
		return "hsla(" + ','.join([str(round(h, 2)), str(round(s * 100, 2)) + '%', str(round(l * 100, 2)) + '%,']) + str(alpha) + ')'
	else:
		return "hsl(" + ','.join([str(round(h, 2)), str(round(s * 100, 2)) + '%', str(round(l * 100, 2)) + '%']) + ')'

# RGBA to HSL
def RGBA2HSL(selectPart):
	value = ','.join(selectPart.split(',')[:-1]) + ")"
	return RGB2HSL(value)

# RGBA to HSLA
def RGBA2HSLA(selectPart):
	valueArray = selectPart.split(',')
	value = ','.join(valueArray[:-1]) + ")"

	return RGB2HSL(value, True, valueArray[-1][:-1])

# handle hsl
def handleHSL(p, q, t):
	pi = p
	qi = q
	ti = t

	if ti < 0:
		ti += 1
	if ti > 1:
		ti -= 1
	if ti < 0.166666666:
		return pi + (qi - pi) * 6 * ti
	if ti < 0.5:
		return qi
	if ti < 0.666666666:
		return pi + (qi - pi) * (0.666666666 - ti) * 6
	return pi

def HSL2RGB(selectPart, isAlpha = False, alpha = 1):
	valueArray = matchRGBHSLNumber.findall(selectPart)

	r = g = b = None

	h = float(valueArray[0]) / 360
	s = float(valueArray[1].split('%')[0]) / 100
	l = float(valueArray[2].split('%')[0]) / 100

	if len(valueArray) == 4:
		alpha = valueArray[3]

	if s == 0:
		r = g = b = l
	else:
		q = p = None
		if l < 0.5:
			q = l * (1 + s)
		else:
			q = l + s - l * s
		p = 2 * l - q
		r = round(handleHSL(p, q, h + 0.33333333) * 255)
		g = round(handleHSL(p, q, h) * 255)
		b = round(handleHSL(p, q, h - 0.33333333) * 255)

	if isAlpha:
		return "rgba(%d,%d,%d,%s)" % (int(r),int(g),int(b),str(alpha))
	else:
		return "rgb(%d,%d,%d)" % (int(r),int(g),int(b))

switcher = {
	"rgb": {
		"rgb": lambda value: value,
		"rgba": lambda value: RGB_HSL2RGBA_HSLA(value, 'rgb', 'rgba'),
		"hex": RGB2HEX,
		"hsl": RGB2HSL,
		"hsla": lambda value: RGB2HSL(value, True, 1)
	},
	"rgba": {
		"rgb": lambda value: RGBA_HSLA2RGB_HSL(value, 'rgba', 'rgb'),
		"rgba": lambda value: value,
		"hex": RGB2HEX,
		"hsl": RGBA2HSL,
		"hsla": RGBA2HSLA
	},
	"hsl": {
		"rgb": HSL2RGB,
		"rgba": lambda value: HSL2RGB(value, True, 1),
		"hex": lambda value: RGB2HEX(HSL2RGB(value)),
		"hsl": lambda value: value,
		"hsla": lambda value: RGB_HSL2RGBA_HSLA(value, 'hsl', 'hsla'),
	},
	"hsla": {
		"rgb": HSL2RGB,
		"rgba": lambda value: HSL2RGB(value, True),
		"hex": lambda value: RGB2HEX(HSL2RGB(value)),
		"hsl": lambda value: RGBA_HSLA2RGB_HSL(value, 'hsla', 'hsl'),
		"hsla": lambda value: value,
	},
	"hex": {
		"rgb": HEX2RGB,
		"rgba": lambda value: HEX2RGB(value, True),
		"hex": lambda value: value,
		"hsl": lambda value: RGB2HSL(HEX2RGB(value)),
		"hsla": lambda value: RGB_HSL2RGBA_HSLA(RGB2HSL(HEX2RGB(value)), 'hsl', 'hsla'),
	}
}

def covertColor(selectPart, covertModel):
	"""value(selectPart) covert to need model(covertModel)"""
	valueModel = getSelectValueModel(selectPart)
	handleObj = switcher.get(valueModel, {})
	handleFun = handleObj.get(covertModel, lambda: None)

	return handleFun(selectPart)
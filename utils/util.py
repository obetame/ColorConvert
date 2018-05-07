#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import math

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

matchNumber = re.compile(r'\d*\.*\d{1,3}\%*')
isAndroidColor = False

matchRE = {
	"rgb": r'rgb\([\s\.\d,%]*\)',
	"rgba": r'rgba\([\s\.\d,%]*\)',
	"hsl": r'hsl\([\s\.\d,%]*\)',
	"hsla": r'hsla\([\s\.\d,%]*\)',
	"hex": r'#[\da-zA-Z]{3,8}',
	"cmyk": r'cmyk\([\s\.\d,%]*\)',
	"hsv": r'hsv\([\s\.\d,%]*\)',
}

def getSelectValueMode(selectPart):
	"""user select section value mode"""
	value = selectPart.upper()

	if 'RGBA' in value:
		return 'rgba'
	elif 'RGB' in value:
		return 'rgb'
	elif 'HSLA' in value:
		return 'hsla'
	elif 'HSL' in value:
		return 'hsl'
	elif 'CMYK' in value:
		return 'cmyk'
	elif 'HSV' in value:
		return 'hsv'
	else:
		return 'hex'

# handle HEX
def handleHEXValue(part):
	"""
		part -- #fff,#ffffff,#ffffff80,#80ffffff etc..
		return -- ['f','f','f','f','f','f'],['f','f','f','f','f','f','8','0'] etc...
	"""
	if '#' not in part:
		return part

	value = part.split("#")
	if len(value) <= 1:
		value = value[0]
	else:
		value = value[1]

	letters = []

	if len(value) == 3:
		for letter in value:
			letters.append(letter.upper())
			letters.append(letter.upper())
	elif len(value) == 6 or not isAndroidColor:
		for letter in value:
			letters.append(letter.upper())
	elif isAndroidColor:
		for letter in value[2:]:
			letters.append(letter.upper())
		letters.extend(value[:2])

	return letters

def getHexAlphaValue(part):
	"""
		Get hex's transparency value and convert to decimal
		part -- ['f','f','f','f','f','f','f','f']
		return -- 1
	"""
	value = part[-2:]

	a = mapHEX.get(value[1].upper())
	b = mapHEX.get(value[0].upper()) * 16

	return round((a + b) / 255.0, 4)

def getRgbaAlphaValue(part):
	"""
		Get rgba transparency value and convert to hexadecimal
		part -- rgba(1,1,1,.5)
		return '80'
	"""
	alpha = float(part.split(',')[-1].replace(')', ''))
	toDecimal = alpha * 256
	
	if alpha == 1.0 or alpha > 1:
		return 'FF'

	b = int(toDecimal % 16)
	a = int(toDecimal / 16 % 16)

	return mapRGB.get(a) + mapRGB.get(b)

def handleHEXValueString(part, isAndroid = False):
	"""
		part -- #fff,#ffffff,#ffffff80,#80ffffff etc..
		isAndroid -- Android color value hex transparency in front
		return -- #ffffff
	"""
	if '#' not in part:
		return '#' + part.upper()

	value = part.split("#")
	if len(value) <= 1:
		value = value[0]
	else:
		value = value[1]

	letters = '#'

	if len(value) == 3:
		for letter in value:
			letters += letter.upper()
			letters += letter.upper()
	elif len(value) == 6:
		letters = letters + value.upper()
	else:
		# len = 8
		if isAndroid:
			letters = letters + value.upper()[2:]
		else:
			letters = letters + value.upper()[:-2]

	return letters

# handle RGB
def handleRGBValue(selectPart):
	value = matchNumber.findall(selectPart)

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
	value = matchNumber.findall(selectPart)

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
		if len(lettersArray) == 8:
			"""include alpha value"""
			alphaValue = getHexAlphaValue(lettersArray)

			return 'rgba(' + rgb[:-1] + "," + str(alphaValue) + ')'
		else:
			return 'rgba(' + rgb[:-1] + "," + str(alpha) + ')'
	else:
		return 'rgb(' + rgb[:-1] + ')'

# RGB to HEX
def RGB2HEX(selectPart, isAlpha = False):
	numberArray = handleRGBValue(selectPart)

	valueArray = []
	for value in numberArray:
		valueArray.append(value * 255)

	hexValue = '#'
	for n in list(range(0,3)):
		number = valueArray[n]
		if (number == 0):
			hexValue += '00'
			continue

		first = int(number / 16)
		secend = int(number % 16)
		hexValue += (mapRGB[first] + mapRGB[secend])

	if isAlpha and len(numberArray) == 4:
		hexValue += getRgbaAlphaValue(selectPart)

	return hexValue

# RGB to RGBA
def RGB_HSL2RGBA_HSLA(selectPart, input, output):
	value = selectPart[:-1] + ",1)"
	return value.replace(input, output)

# RGBA to RGB
def RGBA_HSLA2RGB_HSL(selectPart, input, output):
	valueArray = selectPart.split(",")
	valueArray[3] = ")"

	return ",".join(valueArray).replace(input, output)[:-2] + ")"

def RGB2HSL(selectPart, isAlpha = False, alpha = 1):
	# RGB to HSL
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
		return "hsla(%s,%s%%,%s%%,%s)" % (str(round(h, 2)), str(round(s * 100, 2)), str(round(l * 100, 2)), str(alpha))
	else:
		return "hsl(%s,%s%%,%s%%)" % (str(round(h, 2)), str(round(s * 100, 2)), str(round(l * 100, 2)))

def RGBA2HSL(selectPart):
	"""RGBA to HSL
	https://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion
	"""
	value = ','.join(selectPart.split(',')[:-1]) + ")"
	return RGB2HSL(value)

def RGBA2HSLA(selectPart):
	# RGBA to HSLA
	valueArray = selectPart.split(',')
	value = ','.join(valueArray[:-1]) + ")"

	return RGB2HSL(value, True, valueArray[-1][:-1])

def handleHSL(p, q, t):
	# handle hsl
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
	# hsl to rgb
	valueArray = matchNumber.findall(selectPart)

	r = g = b = None

	h = float(valueArray[0])
	s = float(valueArray[1].split('%')[0]) / 100
	l = float(valueArray[2].split('%')[0]) / 100

	if h >= 360:
		h -= 360
	h = h / 360

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
		if len(valueArray) == 4:
			return "rgba(%d,%d,%d,%s)" % (int(r),int(g),int(b),valueArray[-1])
		return "rgba(%d,%d,%d,%s)" % (int(r),int(g),int(b),str(alpha))
	else:
		return "rgb(%d,%d,%d)" % (int(r),int(g),int(b))

def RGB2CMYK(selectPart):
	"""RGB TO CMYK
	https://www.rapidtables.com/convert/color/rgb-to-cmyk.html
	"""
	numberArray = handleRGBValue(selectPart)

	r = numberArray[0]
	g = numberArray[1]
	b = numberArray[2]

	k = round(1 - max(numberArray), 3)

	if 1 - k == 0:
		return "cmyk(%s,%s,%s,%s)" % (str(0),str(0),str(0),str(1))

	c = round((1 - r - k) / (1 - k), 3)
	m = round((1 - g - k) / (1 - k), 3)
	y = round((1 - b - k) / (1 - k), 3)

	value = [c,m,y,k]
	for i,n in enumerate(value):
		if n <= 0:
			# fixed "-0.0"
			value[i] = 0

	return "cmyk(%s,%s,%s,%s)" % (str(value[0]),str(value[1]),str(value[2]),str(value[3]))

def CMYK2RGB(selectPart, isAlpha = False, alpha = 1):
	"""CMYK TO RGB
	https://www.rapidtables.com/convert/color/cmyk-to-rgb.html
	"""
	valueArray = matchNumber.findall(selectPart)

	c = float(valueArray[0])
	m = float(valueArray[1])
	y = float(valueArray[2])
	k = float(valueArray[3])

	r = int(round(255 * (1 - c) * (1 - k)))
	g = int(round(255 * (1 - m) * (1 - k)))
	b = int(round(255 * (1 - y) * (1 - k)))

	if isAlpha:
		return "rgba(%d,%d,%d,%s)" % (r,g,b,str(alpha))
	else:
		return "rgb(%d,%d,%d)" % (r,g,b)

def RGB2HSV(selectPart):
	"""RGB TO HSV
	https://www.rapidtables.com/convert/color/rgb-to-hsv.html
	"""
	numberArray = handleRGBValue(selectPart)
	
	# remove alpha
	if len(numberArray) > 3:
		numberArray = numberArray[:-1]

	r = numberArray[0]
	g = numberArray[1]
	b = numberArray[2]
	h = s = v = 0

	cmax = max(numberArray)
	cmin = min(numberArray)
	mid = cmax - cmin

	if mid == 0:
		h = 0
	elif cmax == r:
		h = 60 * (((g - b) / mid) % 6)
	elif cmax == g:
		h = 60 * ((b - r) / mid + 2)
	elif cmax == b:
		h = 60 * ((r - g) / mid + 4)

	if cmax == 0:
		s = 0
	else:
		s = mid / cmax

	v = cmax

	return "hsv(%d,%s%%,%s%%)" % (h,str(round(s * 100, 2)),str(round(v * 100, 2)))

def HSV2RGB(selectPart, isAlpha = False, alpha = 1):
	"""HSV TO RGB
	https://www.rapidtables.com/convert/color/hsl-to-rgb.html
	"""
	valueArray = matchNumber.findall(selectPart)

	h = float(valueArray[0])
	s = float(valueArray[1].split('%')[0]) / 100
	v = float(valueArray[2].split('%')[0]) / 100

	if h >= 360:
		h -= 360

	c = v * s
	x = c * (1 - math.fabs((h / 60) % 2 - 1))
	m = v - c

	r = g = b = 0

	if h >= 0 and h < 60:
		r = c
		g = x
		b = 0
	elif h >= 60 and h < 120:
		r = x
		g = c
		b = 0
	elif h >= 120 and h < 180:
		r = 0
		g = c
		b = x
	elif h >= 180 and h < 240:
		r = 0
		g = x
		b = c
	elif h >= 240 and h < 300:
		r = x
		g = 0
		b = c
	elif h >= 300 and h < 360:
		r = c
		g = 0
		b = x

	R = round((r + m) * 255)
	G = round((g + m) * 255)
	B = round((b + m) * 255)

	if isAlpha:
		return "rgba(%d,%d,%d,%s)" % (R,G,B, str(alpha))
	else:
		return "rgb(%d,%d,%d)" % (R,G,B)

switcher = {
	"rgb": {
		"rgb": lambda value: value,
		"rgba": lambda value: RGB_HSL2RGBA_HSLA(value, 'rgb', 'rgba'),
		"hex": RGB2HEX,
		"hsl": RGB2HSL,
		"hsla": lambda value: RGB2HSL(value, isAlpha = True),
		"cmyk": RGB2CMYK,
		"hsv": RGB2HSV
	},
	"rgba": {
		"rgb": lambda value: RGBA_HSLA2RGB_HSL(value, 'rgba', 'rgb'),
		"rgba": lambda value: value,
		"hex": lambda value: RGB2HEX(value, isAlpha = True),
		"hsl": RGBA2HSL,
		"hsla": RGBA2HSLA,
		"cmyk": RGB2CMYK,
		"hsv": RGB2HSV
	},
	"hsl": {
		"rgb": HSL2RGB,
		"rgba": lambda value: HSL2RGB(value, isAlpha = True),
		"hex": lambda value: RGB2HEX(HSL2RGB(value)),
		"hsl": lambda value: value,
		"hsla": lambda value: RGB_HSL2RGBA_HSLA(value, 'hsl', 'hsla'),
		"cmyk": lambda value: RGB2CMYK(HSL2RGB(value)),
		"hsv": lambda value: RGB2HSV(HSL2RGB(value))
	},
	"hsla": {
		"rgb": HSL2RGB,
		"rgba": lambda value: HSL2RGB(value, isAlpha = True),
		"hex": lambda value: RGB2HEX(HSL2RGB(value, isAlpha = True), isAlpha = True),
		"hsl": lambda value: RGBA_HSLA2RGB_HSL(value, 'hsla', 'hsl'),
		"hsla": lambda value: value,
		"cmyk": lambda value: RGB2CMYK(HSL2RGB(value)),
		"hsv": lambda value: RGB2HSV(HSL2RGB(value))
	},
	"hex": {
		"rgb": HEX2RGB,
		"rgba": lambda value: HEX2RGB(value, isAlpha = True),
		"hex": lambda value: value,
		"hsl": lambda value: RGB2HSL(HEX2RGB(value)),
		"hsla": lambda value: RGBA2HSLA(HEX2RGB(value, isAlpha = True)),
		"cmyk": lambda value: RGB2CMYK(HEX2RGB(value)),
		"hsv": lambda value: RGB2HSV(HEX2RGB(value))
	},
	"cmyk": {
		"rgb": CMYK2RGB,
		"rgba": lambda value: CMYK2RGB(value, isAlpha = True),
		"hex": lambda value: RGB2HEX(CMYK2RGB(value)),
		"hsl": lambda value: RGB2HSL(CMYK2RGB(value)),
		"hsla": lambda value: RGB_HSL2RGBA_HSLA(RGB2HSL(CMYK2RGB(value)), 'hsl', 'hsla'),
		"cmyk": lambda value: value,
		"hsv": lambda value: RGB2HSV(CMYK2RGB(value))
	},
	"hsv": {
		"rgb": HSV2RGB,
		"rgba": lambda value: HSV2RGB(value, isAlpha = True),
		"hex": lambda value: RGB2HEX(HSV2RGB(value)),
		"hsl": lambda value: RGB2HSL(HSV2RGB(value)),
		"hsla": lambda value: RGB_HSL2RGBA_HSLA(RGB2HSL(HSV2RGB(value)), 'hsl', 'hsla'),
		"cmyk": lambda value: RGB2CMYK(HSV2RGB(value)),
		"hsv": lambda value: value
	}
}

def convertColor(selectPart, convertMode, isAndroid = False):
	"""value(selectPart) convert to need mode(convertMode)"""
	global isAndroidColor
	isAndroidColor = isAndroid

	valueMode = getSelectValueMode(selectPart)

	if valueMode == 'hex':
		length = len(selectPart)
		if length != 4 and length != 7 and length != 9:
			return None

	handleObj = switcher.get(valueMode, {})
	handleFun = handleObj.get(convertMode, lambda value: value)

	return handleFun(selectPart)

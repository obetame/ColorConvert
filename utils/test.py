#!/usr/bin/python
# -*- coding: UTF-8 -*-

from util import *

testValue = [{
	"value": "rgb(81%,89%,12%)",
	"outputs": [
		"rgb(81%,89%,12%)",
		"rgba(81%,89%,12%,1)",
		"hsl(66.23,77.78%,50.5%)",
		"hsla(66.23,77.78%,50.5%,1)",
		"#CEE21E",
		"cmyk(0.09,0,0.865,0.11)",
		"hsv(66,86.52%,89.0%)"]
}, {
	"value": "rgba(81,89,12,0.3)",
	"outputs": [
		"rgb(81,89,12)",
		"rgba(81,89,12,0.3)",
		"hsl(66.23,76.24%,19.8%)",
		"hsla(66.23,76.24%,19.8%,0.3)",
		"#51590C",
		"cmyk(0.09,0,0.865,0.651)",
		"hsv(73,99.66%,34.9%)"]
}, {
	"value": "rgba(81%,89%,12%,0.3)",
	"outputs": [
		"rgb(81%,89%,12%)",
		"rgba(81%,89%,12%,0.3)",
		"hsl(66.23,77.78%,50.5%)",
		"hsla(66.23,77.78%,50.5%,0.3)",
		"#CEE21E",
		"cmyk(0.09,0,0.865,0.11)",
		"hsv(73,99.87%,89.0%)"]
}, {
	"value": "rgb(81,89,12)",
	"outputs": [
		"rgb(81,89,12)",
		"rgba(81,89,12,1)",
		"hsl(66.23,76.24%,19.8%)",
		"hsla(66.23,76.24%,19.8%,1)",
		"#51590C",
		"cmyk(0.09,0,0.865,0.651)",
		"hsv(66,86.52%,34.9%)"]
}, {
	"value": "hsl(400,100%,50%)",
	"outputs": [
		"rgb(255,170,0)",
		"rgba(255,170,0,1)",
		"hsl(400,100%,50%)",
		"hsla(400,100%,50%,1)",
		"#FFAA00",
		"cmyk(0,0.333,1.0,0)",
		"hsv(40,100.0%,100.0%)"]
}, {
	"value": "hsl(66.23,76.24%,19.8%)",
	"outputs": [
		"rgb(81,89,12)",
		"rgba(81,89,12,1)",
		"hsl(66.23,76.24%,19.8%)",
		"hsla(66.23,76.24%,19.8%,1)",
		"#51590C",
		"cmyk(0.09,0,0.865,0.651)",
		"hsv(66,86.52%,34.9%)"]
}, {
	"value": "hsla(66.23,76.24%,19.8%,1)",
	"outputs": [
		"rgb(81,89,12)",
		"rgba(81,89,12,1)",
		"hsl(66.23,76.24%,19.8%)",
		"hsla(66.23,76.24%,19.8%,1)",
		"#51590C",
		"cmyk(0.09,0,0.865,0.651)",
		"hsv(66,86.52%,34.9%)"]
}, {
	"value": "hsla(66.23,76.24%,19.8%,.3)",
	"outputs": [
		"rgb(81,89,12)",
		"rgba(81,89,12,.3)",
		"hsl(66.23,76.24%,19.8%)",
		"hsla(66.23,76.24%,19.8%,.3)",
		"#51590C",
		"cmyk(0.09,0,0.865,0.651)",
		"hsv(66,86.52%,34.9%)"]
}, {
	"value": "#51590C",
	"outputs": [
		"rgb(81,89,12)",
		"rgba(81,89,12,1)",
		"hsl(66.23,76.24%,19.8%)",
		"hsla(66.23,76.24%,19.8%,1)",
		"#51590C",
		"cmyk(0.09,0,0.865,0.651)",
		"hsv(66,86.52%,34.9%)"]
}, {
	"value": "cmyk(0.09,0,0.865,0.651)",
	"outputs": [
		"rgb(81,89,12)",
		"rgba(81,89,12,1)",
		"hsl(66.23,76.24%,19.8%)",
		"hsla(66.23,76.24%,19.8%,1)",
		"#51590C",
		"cmyk(0.09,0,0.865,0.651)",
		"hsv(66,86.52%,34.9%)"]
}, {
	"value": "hsv(180,100%,50%)",
	"outputs": [
		"rgb(0,128,128)",
		"rgba(0,128,128,1)",
		"hsl(180.0,100.0%,25.1%)",
		"hsla(180.0,100.0%,25.1%,1)",
		"#008080",
		"cmyk(1.0,0,0,0.498)",
		"hsv(180,100%,50%)"]
}, {
	"value": "hsv(400,100%,50%)",
	"outputs": [
		"rgb(128,85,0)",
		"rgba(128,85,0,1)",
		"hsl(39.84,100.0%,25.1%)",
		"hsla(39.84,100.0%,25.1%,1)",
		"#805500",
		"cmyk(0,0.336,1.0,0.498)",
		"hsv(400,100%,50%)"]
}]

covertAllModel = ['rgb', 'rgba', 'hsl', 'hsla', 'hex', 'cmyk', 'hsv']

def test():
	for test in testValue:
		value = test['value']
		outputs = test['outputs']
		for n in range(7):
			output = covertColor(value, covertAllModel[n])
			if (output != outputs[n]):
				print("Covert color: %s, Output value: %s,\nShould be: %s" % (value, output, outputs[n]))
			else:
				# print("Covert color: %s, Output value: %s" % (value, output))
				pass

def testOne(n):
	value = testValue[n]['value']
	outputs = testValue[n]['outputs']
	for n in range(7):
		output = covertColor(value, covertAllModel[n])
		if (output != outputs[n]):
			print("Covert color: %s, Output value: %s,\nShould be: %s" % (value, output, outputs[n]))
		else:
			print("Covert color: %s, Output value: %s" % (value, output))

test()
# testOne(4)
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from util import *

testValue = [{
	"value": "rgb(81%,89%,12%)",
	"outputs": ["rgb(81%,89%,12%)", "rgba(81%,89%,12%,1)", "hsl(66.23,77.78%,50.5%)", "hsla(66.23,77.78%,50.5%,1)", "#CEE21E"]
}, {
	"value": "rgba(81,89,12,0.3)",
	"outputs": ["rgb(81,89,12)", "rgba(81,89,12,0.3)", "hsl(66.23,76.24%,19.8%)", "hsla(66.23,76.24%,19.8%,0.3)", "#51590C"]
}, {
	"value": "rgba(81%,89%,12%,0.3)",
	"outputs": ["rgb(81%,89%,12%)", "rgba(81%,89%,12%,0.3)", "hsl(66.23,77.78%,50.5%)", "hsla(66.23,77.78%,50.5%,0.3)", "#CEE21E"]
}, {
	"value": "rgb(81,89,12)",
	"outputs": ["rgb(81,89,12)", "rgba(81,89,12,1)", "hsl(66.23,76.24%,19.8%)", "hsla(66.23,76.24%,19.8%,1)", "#51590C"]
}, {
	"value": "hsl(66.23,76.24%,19.8%)",
	"outputs": ["rgb(81,89,12)", "rgba(81,89,12,1)", "hsl(66.23,76.24%,19.8%)", "hsla(66.23,76.24%,19.8%,1)", "#51590C"]
}, {
	"value": "hsla(66.23,76.24%,19.8%,1)",
	"outputs": ["rgb(81,89,12)", "rgba(81,89,12,1)", "hsl(66.23,76.24%,19.8%)", "hsla(66.23,76.24%,19.8%,1)", "#51590C"]
}, {
	"value": "hsla(66.23,76.24%,19.8%,.3)",
	"outputs": ["rgb(81,89,12)", "rgba(81,89,12,.3)", "hsl(66.23,76.24%,19.8%)", "hsla(66.23,76.24%,19.8%,.3)", "#51590C"]
}]

covertAllModel = ['rgb', 'rgba', 'hsl', 'hsla', 'hex']

for test in testValue:
	value = test['value']
	outputs = test['outputs']
	for n in range(5):
		output = covertColor(value, covertAllModel[n])
		if (output != outputs[n]):
			print("VALUE: " + value + " TO: " + output + " SHOULD: " + outputs[n])
		else:
			print("VALUE: " + value + " TO: " + output)

# print(HSL2RGB("hsla(66.23,76.24%,19.8%,1)", True))
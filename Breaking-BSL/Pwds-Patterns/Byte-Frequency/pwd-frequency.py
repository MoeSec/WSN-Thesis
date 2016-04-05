#!/usr/bin/python2
##############################################
# File name: pwd-frequency.py
# Author: Mauricio Tellez Nava
# Reference: Serial Bootstrap Loader software 
# for the MSP430 - Chris Liechti, Colin Domoney
# and Travis Goodspeed 
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: 02/18/16
# Description:  Collects the frequency count 
# of the bytes found in the IVT
############################################## 
hexValue=[]
for i in range(0,256):
    	hexValue.append(0)

with open("results.csv","r") as fd:
	for line in fd:
		passHex = line.split(",")
		for i in passHex:
			try:
				hexValue[int(i,0)] += 1
			except ValueError:
				continue
				#do nothing

key = 0
for val in hexValue:
	print format(key,"#04x") +","+ str(val)
	key += 1



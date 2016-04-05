#!/usr/bin/python2
##############################################
# File name: convert-endianess.py
# Author: Mauricio Tellez Nava
# Reference: Serial Bootstrap Loader software 
# for the MSP430 - Chris Liechti, Colin Domoney
# and Travis Goodspeed 
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: March 2016
# Description:  Convert the IVT values to little
# endian (obtains the ISR addresses)
############################################## 
import itertools, time
from collections import Counter


listOfApps = []
listOfIVTs = []

# create a two list of lists
for i in range(0,93):
    listOfApps.append([])
    listOfIVTs.append([])

#append the value to designated positions of all passwords
with open('pwd-samples.csv', 'r') as fd:
    app = 0
    pwdVals = []
    for item in fd:
        pos = 0
        pwdVals = item.split(',')
        for i in pwdVals:
            if pos == 32:
                listOfApps[app].append(i.rstrip())
            else:
                listOfApps[app].append(i)
            pos += 1
        app += 1

app = 0
for appPwd in listOfApps:
    listOfIVTs[app].append(appPwd[0])
    for i in range(1,len(appPwd),2):
        listOfIVTs[app].append(appPwd[i+1] + appPwd[i][2:])
    app += 1

for i in listOfIVTs:
    strOutput = ''
    ##i.sort()
    for d in i:
        strOutput += d + ','
    print strOutput

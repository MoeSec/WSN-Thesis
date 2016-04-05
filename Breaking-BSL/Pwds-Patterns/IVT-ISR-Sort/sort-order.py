#!/usr/bin/python2
##############################################
# File name: sort-order.py
# Author: Mauricio Tellez Nava
# Reference: Serial Bootstrap Loader software 
# for the MSP430 - Chris Liechti, Colin Domoney
# and Travis Goodspeed 
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: 02/18/16
# Description:  Sorts the addresses found in 
# the IVT.
############################################## 
import itertools, time
from collections import Counter

listOfAddress = []
listSortedAddress = []

# create a list of lists
for i in range(0,93):
    listOfAddress.append([])
    listSortedAddress.append([])

#append the value to designated positions of all passwords
with open('IVT-PWD-addresses.csv', 'r') as fd:
    pwdVals = []
    app=0
    for item in fd:
        pos = 0
        pwdVals = item.split(',')
        j =0
        for i in range(0,len(pwdVals)):
	    temp = pwdVals[i] + str(j-1)
            listOfAddress[app].append(temp)
            j += 1
        app += 1

# Print Apps with original pwd size and the reduce-no-duplicates size
app = 0
for i in listOfAddress:
    #noDublipcates = list(set(i))
    sortedApp = i
    sortedApp.sort()
    listSortedAddress[app] = sortedApp
    app += 1
    #print noDublipcates[len(noDublipcates)-1], ",", len(i) - 1, ",", len(noDublipcates) - 1

# Print differences between address
#listOfRede
for i in listSortedAddress:
    strOutput = ''
    for j in i:
        strOutput += j + ","
    print strOutput
    #for d in range(1, len(i) - 2):
     #   diff = int(i[d+1], 0) - int(i[d], 0)
     #   strOutput += str(diff) + ","
    #print i[-1] + ',' + strOutput




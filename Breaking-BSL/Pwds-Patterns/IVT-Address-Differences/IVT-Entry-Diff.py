#!/usr/bin/python2
##############################################
# File name: IVT-Entry-Diff.py
# Author: Mauricio Tellez Nava
# Reference: Serial Bootstrap Loader software 
# for the MSP430 - Chris Liechti, Colin Domoney
# and Travis Goodspeed 
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: 02/18/16
# Description:  Take the difference between 
# the sorted addresses found in the IVT.
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
        for i in range(0,len(pwdVals)):
            listOfAddress[app].append(pwdVals[i])
        app += 1

# Print Apps with original pwd size and the reduce-no-duplicates size
app = 0
for i in listOfAddress:
    sortedApp = i
    sortedApp.sort()
    listSortedAddress[app] = sortedApp
    app += 1


# Print differences between address
#listOfRede
for i in listSortedAddress:
    strOutput = ''
    for d in range(1, len(i) - 2):
        diff = int(i[d+1], 0) - int(i[d], 0)
        strOutput += str(i[d+1])+"-"+str(i[d])+","+hex(diff)+","
    print i[-1] + ',' + strOutput




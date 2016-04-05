#!/usr/bin/python2
##############################################
# File name: IVT-duplicates.py
# Author: Mauricio Tellez Nava
# Reference: Serial Bootstrap Loader software 
# for the MSP430 - Chris Liechti, Colin Domoney
# and Travis Goodspeed 
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: March 2016
# Description:  Gets the number of duplicates 
# found in the IVT of applications
############################################## 
import itertools, time
from collections import Counter

listOfAddress = []
listOfNoDuplicates = []
# create a list of lists
for i in range(0,93):
    listOfAddress.append([])

#append the value to designated positions of all passwords
with open('NEW-IVT-addresses.csv', 'r') as fd:
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
    duplicates = list(set(i))
    print i[0], ",", len(duplicates) - 2,",", (len(i)-1) - (len(duplicates) - 2)



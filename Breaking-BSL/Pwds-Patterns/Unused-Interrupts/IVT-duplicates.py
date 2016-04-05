#!/usr/bin/python2

import itertools, time
from collections import Counter


listOfAddress = []
listOfNoDuplicates = []
# create a list of lists
for i in range(0,93):
    listOfAddress.append([])

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
    duplicates = list(set(i))
    print i[0], ",", len(duplicates) - 2,",", (len(i)-1) - (len(duplicates) - 2)



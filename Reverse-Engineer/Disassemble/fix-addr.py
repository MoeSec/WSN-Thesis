#!/usr/bin/
##############################################
# File name: fix-addr.py
# Author: Mauricio Tellez Nava
# Reference: Serial Bootstrap Loader software 
# for the MSP430 - Chris LieGchti, Colin Domoney
# and Travis Goodspeed 
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: 03/07/16
# Description:  The following script will set
# the approach address value for the instructions
##############################################  
import sys, serial, struct, string, time, os

# Main:
START_ADR = 0x4000

def main():

    newDisassembly = []
    # Get password
    with open(sys.argv[1], 'r') as fd:
        for i in fd.readlines():
            values = i.split(':')
            address = values[0].strip()
            #if address != '':
            try:
                newAddr = hex(int(address,16) + START_ADR)
                if values[1].find("ff ff ff ff") == -1:
                    newDisassembly.append("\t"+str(newAddr)[2:]+": "+values[1])
            except ValueError:
                if i.find("...") == -1:
                    print i.strip('\n')
    for i in newDisassembly:
        print i.strip('\n')

if __name__ == '__main__':
    main()

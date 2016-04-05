#!/bin/bash
##############################################
# File name: get-apps-size.sh
# Author: Mauricio Tellez Nava
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: February 2016
# Description: Gets the size of the binaries 
# of TinyOS sample applications.
##############################################  
for VAR in $(find /opt/tinyos-main/apps/* -name 'Makefile')
do
	pathToFile=`dirname $VAR` #absolute path
	cd $pathToFile
	before1=`dirname $pathToFile` #relative path
	before2=`dirname $before1`     #relative path
	romSize=`make telosb 2>/dev/null | grep "ROM"`
	if [[ $romSize == *"ROM" ]]
	then 	
		printf `basename $before2`-`basename $before1`-`basename $pathToFile`.ihex
		printf ",$romSize\n"
	fi
	make clean > /dev/null
done;

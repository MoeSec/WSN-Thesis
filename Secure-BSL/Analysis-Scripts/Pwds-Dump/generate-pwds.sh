#!/bin/bash
##############################################
# File name: generate-pwds.sh
# Author: Mauricio Tellez Nava
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: March 2016
# Description: Dumps the passwords of TinyOS
# sample applications.
##############################################  
for VAR in $(find /opt/tinyos-main/apps/* -name 'Makefile')
do
	pathToFile=`dirname $VAR` #absolute path
	cd $pathToFile
	before1=`dirname $pathToFile` #relative path
	before2=`dirname $before1`     #relative path
	printf $pathToFile"\n"
	make telosb > /dev/null
	printf `basename $before2`-`basename $before1`-`basename $pathToFile`.ihex, >> ~/Desktop/Results/results.csv
	if test -e "build/telosb/main.ihex"
	then
		python ~/Desktop/Results/secure-bsl.py -I -p build/telosb/main.ihex >> ~/Desktop/Results/results.csv
		printf , >> ~/Desktop/Results/results.csv
		python ~/Desktop/Results/secure-bsl.py -testing123 -I -p build/telosb/main.ihex >> ~/Desktop/Results/results.csv
	else
		printf "error\n" >> ~/Desktop/Results/results.csv
	fi
	make clean > /dev/null
done;

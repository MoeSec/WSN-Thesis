#!/bin/bash
##############################################
# File name: generate-pwds.sh
# Author: Mauricio Tellez Nava
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: 02/18/16
# Description: Dumps the passwords of TinyOS
# sample applications.
##############################################   
for VAR in $(find /opt/tinyos-main/apps/* -name 'Makefile')
do
	pathToFile=`dirname $VAR` #absolute path
	cd $pathToFile
	before1=`dirname $pathToFile` #relative path
	before2=`dirname $before1`     #relative path
	make telosb > /dev/null
	printf `basename $before2`-`basename $before1`-`basename $pathToFile`.ihex, >> ~/Desktop/Memory-Dump/pwds-dumps/results.csv
	if test -e "build/telosb/main.ihex"
	then
		python ~/Desktop/Memory-Dump/pwds-dumps/dump-pwd.py build/telosb/main.ihex >> ~/Desktop/Memory-Dump/pwds-dumps/results.csv
	else
		printf "error\n" >> ~/Desktop/Memory-Dump/pwds-dumps/results.csv
	fi
	make clean > /dev/null
done;

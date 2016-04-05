# WSN-Thesis
Repository includes all scripts, software, and results created during the completion of my thesis

As a Graduate student at JMU, I did a thesis on investigating the security of Wireless Sensor Networks.   The WSN-Thesis 
repository consists of analysis scripts as well as code to implement a secure WSN enviroment. 

Directories:

Analysis-Results
	1. STMS : pcap files of monitiong the STMS network
	2. Secure-BSL : excel files of analysing the random passwords 
	3. tos-BSL : excel files of analysing the IVT passwords 

Breaking-BSL 
  1. Applications-Size : script to get applications binary size
  2. Brute-Force-Time : script to get brute force times
  3. Pwds-Dump : scripts to get passwords from the TinyOS applications
	4. Pwds-Patters : scripts to analyze the passwords (or the IVT values)

Reverse-Engineer
  1. Disassemble : script to convert address of disassemble binaniers
  2. Dump-Firmware : scrip to dump data in MSP430 flash memory
  3. sample : samples of disassembled MSP430 binaries

STMS
  1. IEEE802154 : source code of the Secure Temperature Monitoring System for WSNs (MAC layer implementation)
  2. L1-Secure : source code of the Secure Temperature Monitoring System for WSNs (Physical layer implementation)
  3. PPPSniffer : source code of the packet sniffer sensor application 
  
Secure-BSL 
  1. Analysis-Scripts : scripts used ot analyzed the generated passwords
  2. docs : the documentations of the Secure-BSL software
  3. sample : sample files to generate password
  4. secure-bsl.py : the Secure-BSL software that generates random passwords for the MSP430 MCU
  

contact: telle2mx@dukes.jmu.edu

#!/usr/bin/
##############################################
# File name: dump-firmware.py
# Author: Mauricio Tellez Nava
# Reference: Serial Bootstrap Loader software 
# for the MSP430 - Chris LieGchti, Colin Domoney
# and Travis Goodspeed 
# Email : telle2mx@dukes.jmu.edu
# Course: CS-700 - Thesis Research
# Date: 03/07/16
# Description: Dumps the firmware found in 
# MSP430 flash memory
##############################################   
import sys, serial, struct, string, time, os

# Main:
BSL_SYNC = 0x80
DATA_ACK = 0x90
DATA_NAK = 0xA0
DATA_FRAME = 0x80
CMD_FAILED = 0x70
BSL_RXBLK = 0x14  # upload command
BSL_TXBLK = 0x12  # download command
BSL_TXPWORD = 0x10  # password command
MAX_FRAME_COUNT = 16
DATA_FRAME = 0x80
BSL_CHANGEBAUD = 0x20

serialport = None
seqNo = 0
reqNo = 0

def calcChecksum(data, length):
    """Calculates a checksum of "data"."""
    checksum = 0

    for i in range(length / 2):
        checksum = checksum ^ (ord(data[i * 2]) | (ord(data[i * 2 + 1]) << 8))  # xor-ing
    return 0xffff & (checksum ^ 0xffff)

#Establish Connection to port
def comInit(port):
    global serialport
    serialport = serial.Serial(
        port,
        9600,
        parity=serial.PARITY_EVEN,
        timeout=1
    )
    serialport.flushInput()
    serialport.flushOutput()

# RTS Sync Command
def telosSetSCL(level):
    serialport.setRTS(not level)

#DTR Sync Command
def telosSetSDA(level):
    serialport.setDTR(not level)

#I2C Start
def telosI2CStart():
    telosSetSDA(1)
    telosSetSCL(1)
    telosSetSDA(0)

#I2C Stop
def telosI2CStop():
    telosSetSDA(0)
    telosSetSCL(1)
    telosSetSDA(1)

#I2C Send Bits
def telosI2CWriteBit(bit):
    telosSetSCL(0)
    telosSetSDA(bit)
    time.sleep(2e-6)
    telosSetSCL(1)
    time.sleep(1e-6)
    telosSetSCL(0)

#I2C Send Bytes
def telosI2CWriteByte(byte):
    telosI2CWriteBit(byte & 0x80)
    telosI2CWriteBit(byte & 0x40)
    telosI2CWriteBit(byte & 0x20)
    telosI2CWriteBit(byte & 0x10)
    telosI2CWriteBit(byte & 0x08)
    telosI2CWriteBit(byte & 0x04)
    telosI2CWriteBit(byte & 0x02)
    telosI2CWriteBit(byte & 0x01)
    telosI2CWriteBit(0)  # "acknowledge"

#Sync Command Send
def telosI2CWriteCmd(addr, cmdbyte):
    telosI2CStart()
    telosI2CWriteByte(0x90 | (addr << 1))
    telosI2CWriteByte(cmdbyte)
    telosI2CStop()

#Reset to sync
def telosBReset(invokeBSL=0):
    if invokeBSL:
        telosI2CWriteCmd(0, 1)
        telosI2CWriteCmd(0, 3)
        telosI2CWriteCmd(0, 1)
        telosI2CWriteCmd(0, 3)
        telosI2CWriteCmd(0, 2)
        telosI2CWriteCmd(0, 0)
    else:
        telosI2CWriteCmd(0, 3)
        telosI2CWriteCmd(0, 2)
        telosI2CWriteCmd(0, 0)
        time.sleep(0.250)  # give MSP430's oscillator time to stabilize
    serialport.flushInput()  # clear buffers

# Sync with node for I2C communication
def bslSync(wait=0):
    loopcnt = 5
    while wait or loopcnt:
        loopcnt = loopcnt - 1
        serialport.flushInput()
        serialport.write(chr(BSL_SYNC))
        c = serialport.read(1)
        if c == chr(DATA_ACK):
            #print "Sync complete"
            return
        elif not c:
            if loopcnt > 4:
                print "Timeout retry 1"
            elif loopcnt == 4:
                telosBReset(0)
                telosBReset(1)
            elif loopcnt > 0:
                print "Timeout retry 2"
            else:
                print "Timeout Error"
        else:
            print "Failed to sync"

def comRxHeader():
    global seqNo
    global reqNo
    hdr = serialport.read(1)
    if not hdr:
        print "Header not received"
    rxHeader = ord(hdr) & 0xf0
    rxNum = ord(hdr) & 0x0f
    seqNo = 0
    reqNo = 0
    return rxHeader, rxNum

def comRxFrame(rxNum):
    rxFrame = chr(DATA_FRAME | rxNum)
    rxFrameData = serialport.read(3)
    if len(rxFrameData) != 3:
        print "Timeout 1"
    rxFrame = rxFrame + rxFrameData
    if rxFrame[1] == chr(0) and rxFrame[2] == rxFrame[3]:
        rxLengthCRC = ord(rxFrame[2]) + 2
        rxFrameData = serialport.read(rxLengthCRC)
        if len(rxFrameData) != rxLengthCRC:
            print "Timeout 2"
        rxFrame = rxFrame + rxFrameData
        checksum = calcChecksum(rxFrame, ord(rxFrame[2]) + 4)
        if rxFrame[ord(rxFrame[2])+4] == chr(0xff & checksum) and \
            rxFrame[ord(rxFrame[2])+5] == chr(0xff & (checksum >> 8)):
            return rxFrame
        else:
            print "incorrect checksum"
    else:
        print "error dumping data"


def comTxRx(cmd, dataOut, length):
    global seqNo
    global reqNo
    txFrame = []
    rxHeader = 0
    rxNum = 0

    #convert to array
    dataOut = list(dataOut)

    # ************************ Transmit frame ************************
    # make sure packet has even number of bytes
    if(length % 2) != 0:
        dataOut.append(0xFF)

    #build frame header
    txFrame = "%c%c%c%c" % (DATA_FRAME | seqNo, cmd, len(dataOut), len(dataOut))
    reqNo = (seqNo + 1) % MAX_FRAME_COUNT

    #build frame payload
    txFrame = txFrame + string.join(dataOut,'')
    checkSum = calcChecksum(txFrame,length+4)
    txFrame = txFrame + chr(checkSum & 0xff)
    txFrame = txFrame + chr((checkSum >> 8) & 0xff)
    accessAddr = (0x0212 + (checkSum^0xffff)) & 0xfffe

    # write to mote
    serialport.flushInput()
    for c in txFrame:
        serialport.write(c)

    # ************************ Receive frame ************************
    rxHeader, rxNum = comRxHeader()
    if rxHeader == DATA_ACK:
        if rxNum == reqNo:
            #print "Mote Data Access Success"
            return
    elif rxHeader == DATA_NAK:
        #print "Mote Data Access Failed"
	    return
    elif rxHeader == DATA_FRAME:
        if rxNum == reqNo:
            #print "Binary Data received"
            rxFrame = comRxFrame(rxNum)
            return rxFrame
    elif rxHeader == CMD_FAILED:
        print "Command Sent Failed!"


def bslTxRx(cmd, addr, length=0, blkout=None, wait=0):
    # Write Data to MOTE
    if cmd == BSL_TXBLK:
        # Align to even address
        if (addr % 2) != 0:
            addr = addr - 1
            blkout = chr(0xFF) + blkout
            length = length + 1
        # Length must be even
        if (length % 2) != 0:
            blkout = blkout + chr(0xFF)
            length = length + 1

    # Receive Data from Mote
    elif cmd == BSL_RXBLK:
        if (addr % 2) != 0:
            addr = addr - 1
            length = length + 1
        if (length % 2) != 0:
            length = length + 1

    # Add metadata to fram
    dataOut = struct.pack("<HH", addr, length)

    # Add data to frame
    if blkout:
        dataOut = dataOut + blkout

    # Synchronize with Mote
    bslSync(wait)

    # Send/Receive data to/from Mote
    rxFrame = comTxRx(cmd, dataOut, len(dataOut))
    if rxFrame:
        return rxFrame[4:]
    else:
        return rxFrame


def flashMemoryDump(start, size, wait=0):
    data = ''
    pStart = 0
    maxData = 240-16
    while pStart<size:
        length = maxData
        if pStart+length > size:
            length = size - pStart
        data = data + bslTxRx(BSL_RXBLK,
                        pStart+start,
                        length,
                        wait=wait)[:-2]
        pStart = pStart + length
    return data

def main():

    port = sys.argv[1]

    # connect to mote
    comInit(port)

    # Get password
    with open(sys.argv[2], 'r') as fd:
        passwdHex = fd.read().split()
    pwd = ''
    for i in passwdHex:
        pwd += chr(int(i,0))

    # Get Start Address and Size
    try:
        startAddress = int(sys.argv[3])
        dumpSize = int(sys.argv[4])
    except ValueError:
        try:
            startAddress = int(sys.argv[3],16)
            dumpSize = int(sys.argv[4],16)
        except ValueError:
            print "Invalid start address or size"

    #Set Baudrate
    a,l = 0x87e0, 0x0002
    bslTxRx(BSL_CHANGEBAUD,   #Command: change baudrate
                    a, l)                   #args are coded in adr and len
    time.sleep(0.010)                   #recomended delay
    serialport.setBaudrate(38400)   
    baudrate = 38400

    #Send Password for Full Access
    bslTxRx(BSL_TXPWORD,  # Command: Transmit Password
            0xffe0,  # Address of interupt vectors
            0x0020,  # Number of bytes
            pwd,
            wait=1)

    # Get Flash memory data
    binaryData = flashMemoryDump(startAddress,dumpSize)
    try:
        os.remove("app-bin")
    except OSError:
        pass
    with open("app-bin","w+") as fd:
	for i in binaryData:
	    fd.write(i)

if __name__ == '__main__':
    main()

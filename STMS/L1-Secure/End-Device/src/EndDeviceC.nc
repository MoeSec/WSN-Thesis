#include "profile.h"

module EndDeviceC{
	//General Interfaces 
	uses{
		interface Boot;
		interface Leds;
		interface Timer<TMilli> as SendTimer;
	}
	
	//Radio Interfaces 
	uses{
		interface AMSend;
		interface SplitControl as RadioControl;
		interface Packet;
	}
	
	//Security Interfaces
	uses{
		interface CC2420SecurityMode as CC2420Security;
		interface CC2420Keys;
	}
	
	//Sensor Interfaces
	uses{
		interface Read<uint16_t> as TempRead;
	}
}
implementation{
	
	//variables
	message_t packet;
	uint8_t key[16] = {0x99,0x67,0x7F,0xAF,0xD6,0xAD,0xB7,0x0C,0x59,0xE8,0xD9,0x47,0xC9,0x71,0x15,0x0F};
	
	event void Boot.booted(){
		call RadioControl.start();
	}

	event void RadioControl.startDone(error_t error){
		call CC2420Keys.setKey(1,key);
		// Send temp data every 3 seconds
		call SendTimer.startPeriodic(3000);
	}
	
	event void RadioControl.stopDone(error_t error){}
	
	event void CC2420Keys.setKeyDone(uint8_t keyNo, uint8_t* skey){}
	
	event void SendTimer.fired(){
		if (call TempRead.read() == SUCCESS){
			call CC2420Security.setCtr(&packet,1,0);
			if (call AMSend.send(AM_BROADCAST_ADDR, &packet,sizeof(PayloadMsg_t)) == SUCCESS){
				call Leds.led2Toggle();
			}
		}
		else
			call Leds.led0On(); //error sending data
	}
	
	event void TempRead.readDone(error_t result, uint16_t val){
		PayloadMsg_t * payload = call Packet.getPayload(&packet,sizeof(PayloadMsg_t));
		payload->nodeID = TOS_NODE_ID;
		payload->temp = val;
	}
	
	event void AMSend.sendDone(message_t *msg, error_t error){}	
}

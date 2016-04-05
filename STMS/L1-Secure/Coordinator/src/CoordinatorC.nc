#include "profile.h"
#include <stdio.h>
//#include <string.h>

module CoordinatorC{
	//General Interfaces 
	uses{
		interface Boot;
		interface Leds;
	}
	
	//Radio Interfaces
	uses{
		interface SplitControl as RadioControl;
		interface Receive;
	}
	
	//Security Interfaces 
	uses{
		interface CC2420Keys;
	}
}
implementation{

	//Key
	uint8_t key[16] = {0x99,0x67,0x7F,0xAF,0xD6,0xAD,0xB7,0x0C,0x59,0xE8,0xD9,0x47,0xC9,0x71,0x15,0x0F};
	
	event void Boot.booted(){
		call RadioControl.start();
	}

	event void RadioControl.startDone(error_t error){
		if (error == SUCCESS)
			call CC2420Keys.setKey(1,key);
		else
			call RadioControl.start();
	}

	event void RadioControl.stopDone(error_t error){}
	
	event void CC2420Keys.setKeyDone(uint8_t keyNo, uint8_t* skey){}

	event message_t * Receive.receive(message_t *msg, void *payload, uint8_t len){
		if(len != sizeof(PayloadMsg_t)){
			call Leds.led0On();
			printf("Failed to Receive Temperature Data\r\n");
		}
		else{
			PayloadMsg_t* data = (PayloadMsg_t*)payload;
			uint16_t fahrenheit = -39.3 + (0.018 * data->temp);			
			printf("Room %d current temperature: %d\r\n", data->nodeID, fahrenheit);
   			call Leds.led2Toggle();	
		}
		return msg;
	}
	
}

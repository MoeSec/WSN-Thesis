#include "TKN154.h"
#include "profile.h"
#include <stdio.h>
#include <string.h>

module CoordinatorC{
	//General Interfaces
	uses{
		interface Boot;
		interface Leds;
	}
	
	//IEEE 802.15.4 Interfaces
	uses{
		interface MLME_RESET;
		interface MLME_START;
		interface MLME_ASSOCIATE;
		interface MLME_SET;
		interface MLME_COMM_STATUS;		
	}
	
	//Payload Interfaces 
	uses{
		interface MCPS_DATA;
		interface Packet;
	}
}
implementation{
	//global variables
	ieee154_address_t m_lastDevice;
	uint16_t m_shortAddress;
	uint8_t test = 100; //testing PWD
	
	event void Boot.booted(){
		//initialize MAC interface
		call MLME_RESET.request(TRUE); 
	}
	
	//Reset Confirmation
	event void MLME_RESET.confirm(ieee154_status_t status){
		if(status != IEEE154_SUCCESS)
			return;
		//Coordinator address
		call MLME_SET.macShortAddress(COORDINATOR_ADDRESS);
		//Association Support - True
		call MLME_SET.macAssociationPermit(TRUE);
		//Idle when Mac Rx mode
		call MLME_SET.macRxOnWhenIdle(TRUE);
		//start listening for association requests
		call MLME_START.request(
		                  PAN_ID,           // PANId
                          RADIO_CHANNEL,    // LogicalChannel
                          0,                // ChannelPage,
                          0,                // StartTime,
                          15,               // BeaconOrder
                          15,               // SuperframeOrder
                          TRUE,             // PANCoordinator
                          FALSE,            // BatteryLifeExtension
                          FALSE,            // CoordRealignment
                          NULL,             // no realignment security
                          NULL              // no beacon security
                        );
	}
	
	//Start confirmation
	event void MLME_START.confirm(ieee154_status_t status){
		if (status != IEEE154_SUCCESS){
			call Leds.led0On();
			printf("IEEE 802.15.4 Start - FAILED\r\n");
		}
	}
	
	//Association request sent by end device
	event void MLME_ASSOCIATE.indication (
                          uint64_t DeviceAddress,
                          ieee154_CapabilityInformation_t CapabilityInformation,
                          ieee154_security_t *security
                        ){
		call MLME_ASSOCIATE.response(DeviceAddress, m_shortAddress++, IEEE154_ASSOCIATION_SUCCESSFUL, 0);		
	}
	
	//Association confirm
	event void MLME_ASSOCIATE.confirm(
                          uint16_t AssocShortAddress,
                          uint8_t status,
                          ieee154_security_t *security
                        ){
     	if(status != SUCCESS){
     		call Leds.led0On();
     		printf("IEEE 802.15.4 Association - FAILED\r\n");
     	}
    }
	
	//Communication Status update
	event void MLME_COMM_STATUS.indication (
                          uint16_t PANId,
                          uint8_t SrcAddrMode,
                          ieee154_address_t SrcAddr,
                          uint8_t DstAddrMode,
                          ieee154_address_t DstAddr,
                          ieee154_status_t status,
                          ieee154_security_t *security
                        ){
    	if (status == IEEE154_SUCCESS){
      		// association was successful
		call Leds.led1Toggle();
      		m_lastDevice.extendedAddress = DstAddr.extendedAddress;
    	}
    }
    
    //Receive the temperature data
  	event message_t* MCPS_DATA.indication ( message_t* rFrame){
  		//message_t rFrame = frameR;
  		PayloadMsg_t* payload = call Packet.getPayload(rFrame, sizeof(PayloadMsg_t));
   		uint16_t fahrenheit = -39.3 + (0.018 * payload->temp);			
		printf("Room %d current temperature: %d\r\n", payload->nodeID, fahrenheit);
   		call Leds.led2Toggle();
    		return rFrame;
	}
	
	event void MCPS_DATA.confirm( message_t *msg, 
								  uint8_t msduHandle,
								  ieee154_status_t status,
								  uint32_t timestamp){}
}

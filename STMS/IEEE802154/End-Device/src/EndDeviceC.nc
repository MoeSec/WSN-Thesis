#include "TKN154.h"
#include "profile.h"

module EndDeviceC{
	//General Interfaces
	uses{
		interface Boot;
		interface Leds;
		interface Timer<TMilli> as SendTimer;
	}
	
	//IEEE 802.15.4 Interfaces
	uses{
		interface MLME_RESET;
		interface MLME_SET;
		interface MLME_GET;
		interface MLME_ASSOCIATE;
	}

	//Payload interfaces
	uses{
		interface MCPS_DATA;
		interface IEEE154Frame as Frame;
		interface Packet;
	}

	//Sensor interface
	uses{
		interface Read<uint16_t> as TempRead;
	}
}
implementation{
	//Global Variables
	ieee154_CapabilityInformation_t m_capabilityInformation;
	message_t frame;
	ieee154_address_t coordAdr;	
	
	//Helper methods
	void startApp();
	void sendFrame();
	
	event void Boot.booted(){
		m_capabilityInformation.AlternatePANCoordinator = 0;
    	m_capabilityInformation.DeviceType = 0;
    	m_capabilityInformation.PowerSource = 0;
    	m_capabilityInformation.ReceiverOnWhenIdle = 0;
    	m_capabilityInformation.Reserved = 0;
    	m_capabilityInformation.SecurityCapability = 0;
    	m_capabilityInformation.AllocateAddress = 1;    
    	call MLME_RESET.request(TRUE);
	}
	
	//Initilize MAC interface
	event void MLME_RESET.confirm(ieee154_status_t status)
  	{
    	if (status == IEEE154_SUCCESS)
     		startApp();
     	else
     		call Leds.led0On();
  	}

	void startApp(){
		coordAdr.shortAddress = COORDINATOR_ADDRESS;
		//Association fields
		call MLME_SET.phyCurrentChannel(RADIO_CHANNEL);
    	call MLME_SET.macAutoRequest(FALSE);
    	call MLME_SET.macPANId(PAN_ID);
    	call MLME_SET.macCoordShortAddress(COORDINATOR_ADDRESS);
    	call MLME_ASSOCIATE.request(
        		RADIO_CHANNEL,
          		call MLME_GET.phyCurrentPage(),
          		ADDR_MODE_SHORT_ADDRESS,
          		PAN_ID,
          		coordAdr,
          		m_capabilityInformation,
          		NULL);   
         //Frame fields 
         call Frame.setAddressingFields(
			&frame,
			ADDR_MODE_SHORT_ADDRESS,
			ADDR_MODE_SHORT_ADDRESS,
			PAN_ID,
			&coordAdr,
			NULL);
	}
	
	//Send temperature data to coordinator
	void sendFrame(){
		if (call MCPS_DATA.request(&frame,sizeof(PayloadMsg_t),0,TX_OPTIONS_ACK) == IEEE154_SUCCESS)
			call Leds.led2Toggle();	
	}
	
	// Association confirmation
	event void MLME_ASSOCIATE.confirm    (
                          uint16_t AssocShortAddress,
                          uint8_t status,
                          ieee154_security_t *security
                        ){
    	if ( status == IEEE154_SUCCESS ){
      		call Leds.led1On();
      		//Send data every 5 seconds
      		call SendTimer.startPeriodic(5000);
 		}    
 		else
 			startApp(); 		
	}
	
	//read temperature from sensor and send data
	event void SendTimer.fired(){
		if(call TempRead.read() == SUCCESS)
			sendFrame();
		else
			call Leds.led0On(); //sensor read error
	}
	
	//Data received confirmation
	event void MCPS_DATA.confirm( message_t *msg, 
								  uint8_t msduHandle,
								  ieee154_status_t status,
								  uint32_t timestamp){
		if(status == IEEE154_SUCCESS)
			call Leds.led2Off();		
		else
			sendFrame();
	}

	//Capture temperature using sensor 
	event void TempRead.readDone(error_t result, uint16_t val){
		PayloadMsg_t* payload = call Packet.getPayload(&frame, sizeof(PayloadMsg_t));
		payload->nodeID = TOS_NODE_ID;
		payload->temp = val;
	}

	event void MLME_ASSOCIATE.indication (
                          uint64_t DeviceAddress,
                          ieee154_CapabilityInformation_t CapabilityInformation,
                          ieee154_security_t *security){}//success
                          
	event message_t* MCPS_DATA.indication (message_t* r_frame){
    	return r_frame;} //Not Expecting Data
}

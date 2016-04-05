configuration EndDeviceAppC{
}
implementation{
	//General Components
	components MainC;
	components LedsC;
	components EndDeviceC as App;
	components new TimerMilliC();
	App.Boot -> MainC.Boot;
	App.Leds -> LedsC;
	App.SendTimer -> TimerMilliC;
	
	//Radio Components
	components ActiveMessageC;
	App.RadioControl -> ActiveMessageC;
	
	//Security Components 
	components new SecAMSenderC(AM_RADIO_TEMP_MSG) as AMSenderC;
	components CC2420KeysC;
	App.AMSend -> AMSenderC;
	App.Packet -> AMSenderC;
	App.CC2420Security -> AMSenderC;
	App.CC2420Keys -> CC2420KeysC;
	
	//Sensor Components
	components new SensirionSht11C() as TempSensor;
	App.TempRead -> TempSensor.Temperature;
}
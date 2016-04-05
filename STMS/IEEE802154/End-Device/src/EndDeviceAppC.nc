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
	
	// IEEE 802.15.4 Components
	components Ieee802154NonBeaconEnabledC as MAC;
	App.MLME_RESET -> MAC;
	App.MLME_SET -> MAC;
	App.MLME_GET -> MAC;
	App.MLME_ASSOCIATE -> MAC;
	
	// Payload components
	App.MCPS_DATA -> MAC;
	App.Frame -> MAC;
	App.Packet -> MAC;

	// Sensor wiring
	components new SensirionSht11C() as TempSensor;
	App.TempRead -> TempSensor.Temperature;
	
}
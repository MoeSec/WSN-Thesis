configuration CoordinatorAppC{
}
implementation{
	//General Components
	components MainC;
	components LedsC;
	components CoordinatorC as App;
	App.Boot -> MainC.Boot;
	App.Leds -> LedsC;
	
	//Serial Printf components
	components SerialPrintfC;

	//IEEE 802.15.4 Components
	components Ieee802154NonBeaconEnabledC as MAC;
	App.MLME_RESET -> MAC;
	App.MLME_START -> MAC;
	App.MLME_ASSOCIATE -> MAC;
	App.MLME_SET -> MAC;
	App.MLME_COMM_STATUS -> MAC;
	
	//Payload components
	App.MCPS_DATA -> MAC;
	App.Packet -> MAC;
}
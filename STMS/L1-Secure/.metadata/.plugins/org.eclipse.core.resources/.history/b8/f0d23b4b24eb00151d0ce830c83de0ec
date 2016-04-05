configuration CoordinatorAppC{
}
implementation{
	//General Components
	components MainC;
	components LedsC;
	components CoordinatorC as App;
	App.Boot -> MainC.Boot;
	App.Leds -> LedsC;
	
	//Radio Components
	components ActiveMessageC;
	components new AMReceiverC(AM_RADIO_TEMP_MSG);
	App.RadioControl -> ActiveMessageC;
	App.Receive -> AMReceiverC;
	
	//Security Components
	components CC2420KeysC;
	App.CC2420Keys -> CC2420KeysC;
	
	//Serial Print Interface
	components SerialPrintfC;
}
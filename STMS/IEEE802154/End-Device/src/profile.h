#ifndef PROFILE_H
#define PROFILE_H

typedef nx_struct PayloadMsg{
	nx_uint16_t nodeID;
	nx_uint16_t temp;
} PayloadMsg_t;

enum {
  RADIO_CHANNEL = 26,
  PAN_ID = 0x1234,
  COORDINATOR_ADDRESS = 0x9999,
};

#endif /* PROFILE_H */

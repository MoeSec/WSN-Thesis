#ifndef PROFILE_H
#define PROFILE_H

typedef nx_struct PayloadMsg{
	nx_uint16_t nodeID;
	nx_uint16_t temp;
} PayloadMsg_t;

enum{
	AM_RADIO_TEMP_MSG = 6,
};

#endif /* PROFILE_H */

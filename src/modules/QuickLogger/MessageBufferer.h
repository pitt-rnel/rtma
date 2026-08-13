// CMessageBufferer - derived from CMessageBuffer. Provides
// an interface to store RTMA CMessage objects into the
// message buffer defined by the base class.
//
// Meel Velliste 12/23/2008

#ifndef _MESSAGE_BUFFERER_H_
#define _MESSAGE_BUFFERER_H_

#include "MessageBuffer.h"
#include <UPipe.h>
#include <RTMA.h>
#include <RTMA_types.h>

class CMessageBufferer : public CMessageBuffer {
public:
	CMessageBufferer( ) {
		TRY {
		} CATCH_and_THROW( "CMessageBufferer::CMessageBufferer( )");
	}
	~CMessageBufferer( ) {
	}
	int SaveMessage( CMessage *M)
	{
		TRY {
			// Check to make sure we have room in buffers
			if( NumMessages >= NumPreallocMessages) return -1;
			if( TotalDataBytes + M->num_data_bytes > NumPreallocDataBytes) return -2;
			// Store header in buffer
			RTMA_MSG_HEADER *header = (RTMA_MSG_HEADER*) M;
			RTMA_MSG_HEADER *buffer_headers = (RTMA_MSG_HEADER*) Header;
			buffer_headers[NumMessages] = *header;
			// Store data block offset in buffer
			DataBlockOffsets[NumMessages] = TotalDataBytes;
			// Store data block in buffer
			char *pData = Data + TotalDataBytes;
			M->GetData( pData);
			// Increment counters that keep track of how much data we have
			NumMessages++;
			TotalDataBytes += M->num_data_bytes;
			return 0;
		} CATCH_and_THROW( "CMessageBufferer::SaveMessage( CMessage *M)");
	}
};

#endif

/*
 *  QuickLogger - Logs RTMA messages in an attempt to save data for the experiment
 *  Meel Velliste 10/28/2008
 *  
 */

/* ----------------------------------------------------------------------------
   |                              INCLUDES                                    |
   ----------------------------------------------------------------------------*/
#include "RTMA.h"
#include "MessageBufferer.h"

/* ----------------------------------------------------------------------------
   |                       GENERAL DEFINES                                    |
   ----------------------------------------------------------------------------*/
// Default size of message buffers to pre-allocate
// (can be overridden by command-line arguments)
#define QL_NUM_PREALLOC_MESSAGES   1000000   // 1,000,000 messages
#define QL_NUM_PREALLOC_DATABYTES  250000000 // 250 MB of data, should be enough for a few minutes

/* ----------------------------------------------------------------------------
   |                       QUICK Logger MODULE CODE                             |
   ----------------------------------------------------------------------------*/

class CQuickLogger : public RTMA_Module
{
private:
	CMessageBufferer _MessageBufrr;
	bool _logging;
public:
	CQuickLogger();
	~CQuickLogger();

	void MainFunction( void);

private:
	void Status(const MyCString& msg);
	void DumpBuffer( char *Filename);
    void AutoDumpBuffer();
};

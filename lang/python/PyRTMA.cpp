// Andrew S. Whitford 01/09 asw35
#include "PyRTMA.h"


/// Destructor. RTMA cleanup.
PyRTMA::~PyRTMA(void)
{
    EndModule();

 return;
}


/// Initializes a connection to RTMA and subscribes to relevant message types.
void
PyRTMA::InitializeAndSubscribe(MODULE_ID moduleid, MSG_TYPE* types,
                               unsigned num_types)
{
    try
    {
        mid = moduleid;
        RTMA_Module::InitVariables(mid, HID);
        BeginModule(types, num_types); // Might want to just connect.
    }
    catch(MyCException& e)
    {
        e.AddToStack("PyRTMA::InitializeAndSubscribe");
        e.ReportToFile(const_cast<char*>(LOG_FILENAME));
        throw e;
    }

 return;
}


/// Send a signal (a message with no data) to all RTMA modules. Does not
/// (yet) reproduce the capability to send signals to specific modules.
void
PyRTMA::Signal(int type)
{
    try { SendSignal(type); }
    catch(MyCException& e)
    {
        e.AddToStack("PyRTMA::Signal");
        e.ReportToFile(const_cast<char*>(LOG_FILENAME));
        throw e;
    }

 return;
}


/// Send a message to all RTMA modules.
void
PyRTMA::Send(int type, void *data, unsigned size)
{
    try
    {
        CMessage ms(type, data, size);
        SendMessage(&ms);
    }
    catch(MyCException& e)
    {
        e.AddToStack("PyRTMA::Send");
        e.ReportToFile(const_cast<char*>(LOG_FILENAME));
        throw e;
    }

 return;
}


/// Read an RTMA message. If no argument is provided, then the timeout defaults
/// to a value of -1, which signals a blocking read. A timeout of 0 signals a
/// non-blocking read. If the timeout is positive, then ReadMessage blocks for
/// up to timeout seconds.
MSG_TYPE
PyRTMA::Read(double timeoutS) 
{
    // ReadMessage returns 1 if a message was read, and 0 if no message is
    // available.
    try { ReadMessage(&mr, timeoutS); }
    catch(MyCException& e)
    {
        e.AddToStack("PyRTMA::Read");
        e.ReportToFile(const_cast<char*>(LOG_FILENAME));
        throw e;
    }

 return mr.msg_type;
}


/// Retrieves the MDF for the last message that was read.
void
PyRTMA::GetMessageData(void* buffer, unsigned buffer_size)
{
    try
    {
        if(mr.num_data_bytes <= buffer_size)
            mr.GetData(buffer);
        else
            throw MyCException("Data buffer too small");
    }
    catch(MyCException& e)
    {
        e.AddToStack("PyRTMA::GetMessageData");
        e.ReportToFile(const_cast<char*>(LOG_FILENAME));
        throw e;
    }

 return;
}



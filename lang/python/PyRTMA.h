// Andrew S. Whitford 01/09 asw35

#include "../../../include/RTMA_AppModule.h"


/// RTMA module class designed to facilitate the generation of a Python-RTMA
/// interface with SWIG.
class PyRTMA : public RTMA_AppModule
{
  public:
    static const HOST_ID HID = HID_LOCAL_HOST;
    static const char LOG_FILENAME[];

  private:
    MODULE_ID mid;
    CMessage mr;

  public:
    // Constructors and destructors.
    ~PyRTMA(void);

    // RTMA initialization utility function.
    void InitializeAndSubscribe(MODULE_ID, MSG_TYPE*, unsigned)
            throw(MyCException);

    // RTMA messaging wrappers.
    void Signal(int) throw(MyCException);
    void Send(int, void*, unsigned) throw(MyCException);
    MSG_TYPE Read(double timeoutMs=-1) throw(MyCException);
    void GetMessageData(void*, unsigned) throw(MyCException);

    // Inherited from RTMA_AppModule.
    void MainFunction(void) {;}
    void EventHook(CMessage*) {;}
    void CleanOnExit(void) {;}
    void CleanOnKill(void) {;}
};


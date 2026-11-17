QuickLogger - logs every RTMA message in memory, and saves the log on request.

    QuickLogger [SERVER]

SERVER is the message manager's address, host:port, as for
RTMA_Module::ConnectToMMM(). The default is localhost:7111.

QuickLogger connects as module 5 (MID_QUICK_LOGGER) with the name QuickLogger,
subscribes to every message type, and sends LM_READY when it is recording. It
acts on these messages, from any module:

    SAVE_MESSAGE_LOG          save the log to the file named, then clear it,
                              and send MESSAGE_LOG_SAVED. A log that can't be
                              saved is kept, and the error logged.
    PAUSE_MESSAGE_LOGGING     stop adding messages to the log
    RESUME_MESSAGE_LOGGING    start again
    RESET_MESSAGE_LOG         clear the log
    DUMP_MESSAGE_LOG          save the log to a timestamped QuickLogger.Dump file
    LM_EXIT                   exit

The files are QuickLogger version 1 files, which LogReader (MATLAB) and
pyrtma's LogReader read.

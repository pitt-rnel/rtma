#!/usr/bin/python
from __future__ import print_function
import time
import PyRTMA
from PyRTMA import copy_from_msg
import message_defs as mdefs
import sys

MID_CONSUMER = 11

if __name__ == "__main__":
    mod = PyRTMA.RTMA_Module(MID_CONSUMER, 0)
    mod.ConnectToMMM("localhost:7111")
    mod.Subscribe(mdefs.MT_TEST_DATA)
    
    print("Consumer running...\n")
    
    while (1):
        msg = PyRTMA.CMessage()
        mod.ReadMessage(msg)    # blocking read
        print("Received message ", msg.GetHeader().msg_type)

        if msg.GetHeader().msg_type == mdefs.MT_TEST_DATA:
            msg_data = mdefs.MDF_TEST_DATA()
            copy_from_msg(msg_data, msg)
            print("  Data = [a: %d, b: %d, x: %f]" % (msg_data.a, msg_data.b, msg_data.x))
        
    mod.DisconnectFromMMM()
        

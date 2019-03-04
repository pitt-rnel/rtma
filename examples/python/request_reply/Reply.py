#!/usr/bin/python
from __future__ import print_function
import time
import PyRTMA
from PyRTMA import copy_from_msg, copy_to_msg, MT_EXIT, MT_KILL
import message_defs as mdefs
import sys

MID_REPLY = 10

# Note: Reply must be started first

if __name__ == "__main__":
    mod = PyRTMA.RTMA_Module(MID_REPLY, 0)
    mod.ConnectToMMM()
    mod.Subscribe(mdefs.MT_REQUEST_TEST_DATA)
    
    print("Reply running...\n")
    
    run = True
    while run:
        in_msg = PyRTMA.CMessage()
        print("Waiting for message")
        rcv = mod.ReadMessage(in_msg, 1.0)
        if rcv == 1:
            print("Received message", in_msg.GetHeader().msg_type)
            out_msg = PyRTMA.CMessage(mdefs.MT_TEST_DATA)
            data = mdefs.MDF_TEST_DATA()
            if in_msg.GetHeader().msg_type == mdefs.MT_REQUEST_TEST_DATA:
                data.a = -20
                data.b = 47
                data.x = 123.456
                copy_to_msg(data, out_msg)
                mod.SendMessage(out_msg)
                print("Sent message", out_msg.GetHeader().msg_type)
            elif in_msg.GetHeader().msg_type in (MT_EXIT, MT_KILL):
               run = False        

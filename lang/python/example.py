#!/usr/bin/python
import time
import PyRTMA
from PyRTMA import copy_from_msg, copy_to_msg, MT_EXIT, MT_KILL
import RTMA_types
import numpy as np
import sys

MID_PRODUCER = 10
MID_CONSUMER = 11
MT_REQUEST_TEST_DATA = 101
MT_TEST_DATA = 102
    

def test_producer(server=""):
    mod = PyRTMA.RTMA_Module(MID_PRODUCER, 0)
    if len(server) > 0:
        print server
        mod.ConnectToMMM(server)
    else:
        print "Got here"
        mod.ConnectToMMM()
        
    mod.Subscribe(MT_REQUEST_TEST_DATA)
    mod.Subscribe(MT_EXIT)
    mod.Subscribe(MT_KILL)
    mod.SendModuleReady()
    run = True
    while run:
        in_msg = PyRTMA.CMessage()
        print "Waiting for message"
        mod.ReadMessage(in_msg)
        print "Received message", in_msg.GetHeader().msg_type
        out_msg = PyRTMA.CMessage(MT_TEST_DATA)
        data = RTMA_types.MDF_TEST_DATA()
        if in_msg.GetHeader().msg_type == MT_REQUEST_TEST_DATA:
            data.a = -20
            data.b = 47
            data.x = 123.456
            copy_to_msg(data, out_msg)
            mod.SendMessageRTMA(out_msg)
            print "Sent message", out_msg.GetHeader().msg_type
        elif in_msg.GetHeader().msg_type in (MT_EXIT, MT_KILL):
           run = False


# consumer must be started second
def test_consumer(server=""):
    mod = PyRTMA.RTMA_Module(MID_CONSUMER, 0)
    if len(server) > 0:
        print server
        mod.ConnectToMMM(server)
    else:
        mod.ConnectToMMM()
    mod.Subscribe(MT_TEST_DATA)
    mod.Subscribe(MT_EXIT)
    mod.Subscribe(MT_KILL)
    mod.SendModuleReady()
    for i in range(10):
        mod.SendSignal(MT_REQUEST_TEST_DATA)
        print("Sent request for data")
        msg = PyRTMA.CMessage()
        mod.ReadMessage(msg)
        print "Received message", msg.GetHeader().msg_type
        msg_data = RTMA_types.MDF_TEST_DATA()
        copy_from_msg(msg_data, msg)
        print "Data = [a: %d, b: %d, x: %f]" % \
            (msg_data.a, msg_data.b, msg_data.x)
        time.sleep(1)
    mod.DisconnectFromMMM()
    return msg


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'producer':
            msg = test_producer()
        elif sys.argv[1] == 'consumer':
            msg = test_consumer()
        elif sys.argv[1] == 'test':
            i,o = test_pass()
#     else:
#         print "Need a command-line argument that specifies 'producer'" \
#             "or 'consumer'"
        

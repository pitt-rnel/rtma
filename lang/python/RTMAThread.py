from time import sleep
from threading import Thread
from PyRTMA import RTMA_Module, CMessage
import RTMA_config as rc

class Subscription(object):
    def __init__(self, name, num=None, has_data=True):
        self.name = name
        if num == None:
            self.num = eval('rc.MT_%s' % name)
        else:
            if not type(num) == int:
                raise ValueError("Subscription number must be of type `int`")
            self.num = num
        if has_data:
            mdf_name = 'MDF_%s' % (name)
            self.mdf = eval('rc.' + mdf_name)
        else:
            self.mdf = None
            
class RTMAThread(Thread):
    def run(self):
        mod = RTMA_Module(self.mid, 0)
        mod.ConnectToMMM()
        for sub in self.subs:
            print "subscribing to %s" % (sub)
            mod.Subscribe(sub)
        mod.SendModuleReady()
        while (self.status()):
            msg = CMessage()
            rcv = mod.ReadMessage(msg, 0)
            if rcv == 1:
                if msg.GetHeader().msg_type in self.subs:
                    self.recv_msg(msg)
            sleep(.001)

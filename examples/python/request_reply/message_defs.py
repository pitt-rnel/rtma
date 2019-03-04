from ctypes import *



class MDF_TEST_DATA(Structure):
    pass
MDF_TEST_DATA._pack_ = 4
MDF_TEST_DATA._fields_ = [
    ('a', c_int),
    ('b', c_int),
    ('x', c_double),
]
MT_TEST_DATA = 102 # Variable c_int '102'
MID_REPLY = 13 # Variable c_int '13'
MID_REQUEST = 12 # Variable c_int '12'
MT_REQUEST_TEST_DATA = 101 # Variable c_int '101'
__all__ = ['MT_TEST_DATA', 'MID_REPLY', 'MID_REQUEST',
           'MDF_TEST_DATA', 'MT_REQUEST_TEST_DATA']

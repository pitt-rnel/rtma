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
MT_REQUEST_TEST_DATA = 101 # Variable c_int '101'
__all__ = ['MT_TEST_DATA', 'MDF_TEST_DATA', 'MT_REQUEST_TEST_DATA']

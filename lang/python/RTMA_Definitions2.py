# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.0
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')

# Import the low-level C/C++ module
if __package__ or '.' in __name__:
    from . import _RTMA_Definitions2
else:
    import _RTMA_Definitions2

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == "thisown":
        return self.this.own(value)
    if name == "this":
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static:
        object.__setattr__(self, name, value)
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == "thisown":
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


MAX_MODULES = _RTMA_Definitions2.MAX_MODULES
DYN_MOD_ID_START = _RTMA_Definitions2.DYN_MOD_ID_START
MAX_HOSTS = _RTMA_Definitions2.MAX_HOSTS
MAX_MESSAGE_TYPES = _RTMA_Definitions2.MAX_MESSAGE_TYPES
MIN_STREAM_TYPE = _RTMA_Definitions2.MIN_STREAM_TYPE
MAX_TIMERS = _RTMA_Definitions2.MAX_TIMERS
MAX_INTERNAL_TIMERS = _RTMA_Definitions2.MAX_INTERNAL_TIMERS
MAX_RTMA_MSG_TYPE = _RTMA_Definitions2.MAX_RTMA_MSG_TYPE
MAX_RTMA_MODULE_ID = _RTMA_Definitions2.MAX_RTMA_MODULE_ID
class RTMA_MSG_HEADER(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    msg_type = property(_RTMA_Definitions2.RTMA_MSG_HEADER_msg_type_get, _RTMA_Definitions2.RTMA_MSG_HEADER_msg_type_set)
    msg_count = property(_RTMA_Definitions2.RTMA_MSG_HEADER_msg_count_get, _RTMA_Definitions2.RTMA_MSG_HEADER_msg_count_set)
    send_time = property(_RTMA_Definitions2.RTMA_MSG_HEADER_send_time_get, _RTMA_Definitions2.RTMA_MSG_HEADER_send_time_set)
    recv_time = property(_RTMA_Definitions2.RTMA_MSG_HEADER_recv_time_get, _RTMA_Definitions2.RTMA_MSG_HEADER_recv_time_set)
    src_host_id = property(_RTMA_Definitions2.RTMA_MSG_HEADER_src_host_id_get, _RTMA_Definitions2.RTMA_MSG_HEADER_src_host_id_set)
    src_mod_id = property(_RTMA_Definitions2.RTMA_MSG_HEADER_src_mod_id_get, _RTMA_Definitions2.RTMA_MSG_HEADER_src_mod_id_set)
    dest_host_id = property(_RTMA_Definitions2.RTMA_MSG_HEADER_dest_host_id_get, _RTMA_Definitions2.RTMA_MSG_HEADER_dest_host_id_set)
    dest_mod_id = property(_RTMA_Definitions2.RTMA_MSG_HEADER_dest_mod_id_get, _RTMA_Definitions2.RTMA_MSG_HEADER_dest_mod_id_set)
    num_data_bytes = property(_RTMA_Definitions2.RTMA_MSG_HEADER_num_data_bytes_get, _RTMA_Definitions2.RTMA_MSG_HEADER_num_data_bytes_set)
    remaining_bytes = property(_RTMA_Definitions2.RTMA_MSG_HEADER_remaining_bytes_get, _RTMA_Definitions2.RTMA_MSG_HEADER_remaining_bytes_set)
    is_dynamic = property(_RTMA_Definitions2.RTMA_MSG_HEADER_is_dynamic_get, _RTMA_Definitions2.RTMA_MSG_HEADER_is_dynamic_set)
    reserved = property(_RTMA_Definitions2.RTMA_MSG_HEADER_reserved_get, _RTMA_Definitions2.RTMA_MSG_HEADER_reserved_set)

    def __init__(self):
        _RTMA_Definitions2.RTMA_MSG_HEADER_swiginit(self, _RTMA_Definitions2.new_RTMA_MSG_HEADER())
    __swig_destroy__ = _RTMA_Definitions2.delete_RTMA_MSG_HEADER

# Register RTMA_MSG_HEADER in _RTMA_Definitions2:
_RTMA_Definitions2.RTMA_MSG_HEADER_swigregister(RTMA_MSG_HEADER)

MAX_CONTIGUOUS_MESSAGE_DATA = _RTMA_Definitions2.MAX_CONTIGUOUS_MESSAGE_DATA
class RTMA_MESSAGE(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    msg_type = property(_RTMA_Definitions2.RTMA_MESSAGE_msg_type_get, _RTMA_Definitions2.RTMA_MESSAGE_msg_type_set)
    msg_count = property(_RTMA_Definitions2.RTMA_MESSAGE_msg_count_get, _RTMA_Definitions2.RTMA_MESSAGE_msg_count_set)
    send_time = property(_RTMA_Definitions2.RTMA_MESSAGE_send_time_get, _RTMA_Definitions2.RTMA_MESSAGE_send_time_set)
    recv_time = property(_RTMA_Definitions2.RTMA_MESSAGE_recv_time_get, _RTMA_Definitions2.RTMA_MESSAGE_recv_time_set)
    src_host_id = property(_RTMA_Definitions2.RTMA_MESSAGE_src_host_id_get, _RTMA_Definitions2.RTMA_MESSAGE_src_host_id_set)
    src_mod_id = property(_RTMA_Definitions2.RTMA_MESSAGE_src_mod_id_get, _RTMA_Definitions2.RTMA_MESSAGE_src_mod_id_set)
    dest_host_id = property(_RTMA_Definitions2.RTMA_MESSAGE_dest_host_id_get, _RTMA_Definitions2.RTMA_MESSAGE_dest_host_id_set)
    dest_mod_id = property(_RTMA_Definitions2.RTMA_MESSAGE_dest_mod_id_get, _RTMA_Definitions2.RTMA_MESSAGE_dest_mod_id_set)
    num_data_bytes = property(_RTMA_Definitions2.RTMA_MESSAGE_num_data_bytes_get, _RTMA_Definitions2.RTMA_MESSAGE_num_data_bytes_set)
    remaining_bytes = property(_RTMA_Definitions2.RTMA_MESSAGE_remaining_bytes_get, _RTMA_Definitions2.RTMA_MESSAGE_remaining_bytes_set)
    is_dynamic = property(_RTMA_Definitions2.RTMA_MESSAGE_is_dynamic_get, _RTMA_Definitions2.RTMA_MESSAGE_is_dynamic_set)
    reserved = property(_RTMA_Definitions2.RTMA_MESSAGE_reserved_get, _RTMA_Definitions2.RTMA_MESSAGE_reserved_set)
    data = property(_RTMA_Definitions2.RTMA_MESSAGE_data_get, _RTMA_Definitions2.RTMA_MESSAGE_data_set)

    def __init__(self):
        _RTMA_Definitions2.RTMA_MESSAGE_swiginit(self, _RTMA_Definitions2.new_RTMA_MESSAGE())
    __swig_destroy__ = _RTMA_Definitions2.delete_RTMA_MESSAGE

# Register RTMA_MESSAGE in _RTMA_Definitions2:
_RTMA_Definitions2.RTMA_MESSAGE_swigregister(RTMA_MESSAGE)

MID_MESSAGE_MANAGER = _RTMA_Definitions2.MID_MESSAGE_MANAGER
MID_COMMAND_MODULE = _RTMA_Definitions2.MID_COMMAND_MODULE
MID_APPLICATION_MODULE = _RTMA_Definitions2.MID_APPLICATION_MODULE
MID_NETWORK_RELAY = _RTMA_Definitions2.MID_NETWORK_RELAY
MID_STATUS_MODULE = _RTMA_Definitions2.MID_STATUS_MODULE
MID_QUICKLOGGER = _RTMA_Definitions2.MID_QUICKLOGGER
HID_LOCAL_HOST = _RTMA_Definitions2.HID_LOCAL_HOST
HID_ALL_HOSTS = _RTMA_Definitions2.HID_ALL_HOSTS
ALL_MESSAGE_TYPES = _RTMA_Definitions2.ALL_MESSAGE_TYPES
MT_EXIT = _RTMA_Definitions2.MT_EXIT
MT_KILL = _RTMA_Definitions2.MT_KILL
MT_ACKNOWLEDGE = _RTMA_Definitions2.MT_ACKNOWLEDGE
MT_FAIL_SUBSCRIBE = _RTMA_Definitions2.MT_FAIL_SUBSCRIBE
class MDF_FAIL_SUBSCRIBE(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod_id = property(_RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_mod_id_get, _RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_mod_id_set)
    reserved = property(_RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_reserved_get, _RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_reserved_set)
    msg_type = property(_RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_msg_type_get, _RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_msg_type_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_swiginit(self, _RTMA_Definitions2.new_MDF_FAIL_SUBSCRIBE())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_FAIL_SUBSCRIBE

# Register MDF_FAIL_SUBSCRIBE in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_FAIL_SUBSCRIBE_swigregister(MDF_FAIL_SUBSCRIBE)

MT_FAILED_MESSAGE = _RTMA_Definitions2.MT_FAILED_MESSAGE
class MDF_FAILED_MESSAGE(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    dest_mod_id = property(_RTMA_Definitions2.MDF_FAILED_MESSAGE_dest_mod_id_get, _RTMA_Definitions2.MDF_FAILED_MESSAGE_dest_mod_id_set)
    reserved = property(_RTMA_Definitions2.MDF_FAILED_MESSAGE_reserved_get, _RTMA_Definitions2.MDF_FAILED_MESSAGE_reserved_set)
    time_of_failure = property(_RTMA_Definitions2.MDF_FAILED_MESSAGE_time_of_failure_get, _RTMA_Definitions2.MDF_FAILED_MESSAGE_time_of_failure_set)
    msg_header = property(_RTMA_Definitions2.MDF_FAILED_MESSAGE_msg_header_get, _RTMA_Definitions2.MDF_FAILED_MESSAGE_msg_header_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_FAILED_MESSAGE_swiginit(self, _RTMA_Definitions2.new_MDF_FAILED_MESSAGE())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_FAILED_MESSAGE

# Register MDF_FAILED_MESSAGE in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_FAILED_MESSAGE_swigregister(MDF_FAILED_MESSAGE)

MT_MM_ERROR = _RTMA_Definitions2.MT_MM_ERROR
MT_MM_INFO = _RTMA_Definitions2.MT_MM_INFO
MT_CONNECT = _RTMA_Definitions2.MT_CONNECT
class MDF_CONNECT(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    logger_status = property(_RTMA_Definitions2.MDF_CONNECT_logger_status_get, _RTMA_Definitions2.MDF_CONNECT_logger_status_set)
    daemon_status = property(_RTMA_Definitions2.MDF_CONNECT_daemon_status_get, _RTMA_Definitions2.MDF_CONNECT_daemon_status_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_CONNECT_swiginit(self, _RTMA_Definitions2.new_MDF_CONNECT())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_CONNECT

# Register MDF_CONNECT in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_CONNECT_swigregister(MDF_CONNECT)

MT_DISCONNECT = _RTMA_Definitions2.MT_DISCONNECT
MT_SUBSCRIBE = _RTMA_Definitions2.MT_SUBSCRIBE
MT_UNSUBSCRIBE = _RTMA_Definitions2.MT_UNSUBSCRIBE
MT_PAUSE_SUBSCRIPTION = _RTMA_Definitions2.MT_PAUSE_SUBSCRIPTION
MT_RESUME_SUBSCRIPTION = _RTMA_Definitions2.MT_RESUME_SUBSCRIPTION
MT_SHUTDOWN_RTMA = _RTMA_Definitions2.MT_SHUTDOWN_RTMA
MT_SHUTDOWN_APP = _RTMA_Definitions2.MT_SHUTDOWN_APP
MT_FORCE_DISCONNECT = _RTMA_Definitions2.MT_FORCE_DISCONNECT
class MDF_FORCE_DISCONNECT(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod_id = property(_RTMA_Definitions2.MDF_FORCE_DISCONNECT_mod_id_get, _RTMA_Definitions2.MDF_FORCE_DISCONNECT_mod_id_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_FORCE_DISCONNECT_swiginit(self, _RTMA_Definitions2.new_MDF_FORCE_DISCONNECT())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_FORCE_DISCONNECT

# Register MDF_FORCE_DISCONNECT in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_FORCE_DISCONNECT_swigregister(MDF_FORCE_DISCONNECT)

MT_CORE_MODULE_REINIT_ACK = _RTMA_Definitions2.MT_CORE_MODULE_REINIT_ACK
MT_MODULE_READY = _RTMA_Definitions2.MT_MODULE_READY
class MDF_MODULE_READY(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    pid = property(_RTMA_Definitions2.MDF_MODULE_READY_pid_get, _RTMA_Definitions2.MDF_MODULE_READY_pid_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_MODULE_READY_swiginit(self, _RTMA_Definitions2.new_MDF_MODULE_READY())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_MODULE_READY

# Register MDF_MODULE_READY in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_MODULE_READY_swigregister(MDF_MODULE_READY)

MT_DYNAMIC_DD_READ_ERR = _RTMA_Definitions2.MT_DYNAMIC_DD_READ_ERR
MT_DEBUG_TEXT = _RTMA_Definitions2.MT_DEBUG_TEXT
MT_AM_EXIT = _RTMA_Definitions2.MT_AM_EXIT
MT_START_APP = _RTMA_Definitions2.MT_START_APP
MT_STOP_APP = _RTMA_Definitions2.MT_STOP_APP
MT_RESTART_APP = _RTMA_Definitions2.MT_RESTART_APP
MT_KILL_APP = _RTMA_Definitions2.MT_KILL_APP
MT_AM_RE_READ_CONFIG_FILE = _RTMA_Definitions2.MT_AM_RE_READ_CONFIG_FILE
MT_AM_GET_APP_NAME = _RTMA_Definitions2.MT_AM_GET_APP_NAME
MT_SLAVE_START_APP = _RTMA_Definitions2.MT_SLAVE_START_APP
MT_SLAVE_START_APP_ACK = _RTMA_Definitions2.MT_SLAVE_START_APP_ACK
class MDF_SLAVE_START_APP_ACK(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    num_remote_hosts = property(_RTMA_Definitions2.MDF_SLAVE_START_APP_ACK_num_remote_hosts_get, _RTMA_Definitions2.MDF_SLAVE_START_APP_ACK_num_remote_hosts_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_SLAVE_START_APP_ACK_swiginit(self, _RTMA_Definitions2.new_MDF_SLAVE_START_APP_ACK())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_SLAVE_START_APP_ACK

# Register MDF_SLAVE_START_APP_ACK in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_SLAVE_START_APP_ACK_swigregister(MDF_SLAVE_START_APP_ACK)

MT_SLAVE_STOP_APP = _RTMA_Definitions2.MT_SLAVE_STOP_APP
MT_SLAVE_KILL_APP = _RTMA_Definitions2.MT_SLAVE_KILL_APP
MT_SLAVE_RESTART_APP = _RTMA_Definitions2.MT_SLAVE_RESTART_APP
MT_AM_ERROR = _RTMA_Definitions2.MT_AM_ERROR
MT_AM_ACKNOWLEDGE = _RTMA_Definitions2.MT_AM_ACKNOWLEDGE
MT_FAIL_START_APP = _RTMA_Definitions2.MT_FAIL_START_APP
MT_FAIL_STOP_APP = _RTMA_Definitions2.MT_FAIL_STOP_APP
MT_FAIL_KILL_APP = _RTMA_Definitions2.MT_FAIL_KILL_APP
MT_APP_START_COMPLETE = _RTMA_Definitions2.MT_APP_START_COMPLETE
MT_APP_SHUTODWN_COMPLETE = _RTMA_Definitions2.MT_APP_SHUTODWN_COMPLETE
MT_APP_RESTART_COMPLETE = _RTMA_Definitions2.MT_APP_RESTART_COMPLETE
MT_APP_KILL_COMPLETE = _RTMA_Definitions2.MT_APP_KILL_COMPLETE
MT_ALL_MODULES_READY = _RTMA_Definitions2.MT_ALL_MODULES_READY
MT_CORE_MODULE_REINIT = _RTMA_Definitions2.MT_CORE_MODULE_REINIT
MT_AM_CONFIG_FILE_DATA = _RTMA_Definitions2.MT_AM_CONFIG_FILE_DATA
MT_AM_APP_NAME = _RTMA_Definitions2.MT_AM_APP_NAME
MT_SLAVE_ALL_MODULES_READY = _RTMA_Definitions2.MT_SLAVE_ALL_MODULES_READY
MT_SLAVE_FAIL_START_APP = _RTMA_Definitions2.MT_SLAVE_FAIL_START_APP
MT_SLAVE_FAIL_STOP_APP = _RTMA_Definitions2.MT_SLAVE_FAIL_STOP_APP
MT_SLAVE_FAIL_KILL_APP = _RTMA_Definitions2.MT_SLAVE_FAIL_KILL_APP
MT_SLAVE_APP_SHUTODWN_COMPLETE = _RTMA_Definitions2.MT_SLAVE_APP_SHUTODWN_COMPLETE
MT_SLAVE_APP_RESTART_COMPLETE = _RTMA_Definitions2.MT_SLAVE_APP_RESTART_COMPLETE
MT_SLAVE_APP_KILL_COMPLETE = _RTMA_Definitions2.MT_SLAVE_APP_KILL_COMPLETE
MT_SLAVE_AM_ERROR = _RTMA_Definitions2.MT_SLAVE_AM_ERROR
MT_APP_ERROR = _RTMA_Definitions2.MT_APP_ERROR
MT_SM_EXIT = _RTMA_Definitions2.MT_SM_EXIT
MT_CLOCK_SYNC = _RTMA_Definitions2.MT_CLOCK_SYNC
MT_TIMER_EXPIRED = _RTMA_Definitions2.MT_TIMER_EXPIRED
class MDF_TIMER_EXPIRED(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    timer_id = property(_RTMA_Definitions2.MDF_TIMER_EXPIRED_timer_id_get, _RTMA_Definitions2.MDF_TIMER_EXPIRED_timer_id_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_TIMER_EXPIRED_swiginit(self, _RTMA_Definitions2.new_MDF_TIMER_EXPIRED())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_TIMER_EXPIRED

# Register MDF_TIMER_EXPIRED in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_TIMER_EXPIRED_swigregister(MDF_TIMER_EXPIRED)

MT_TIMED_OUT = _RTMA_Definitions2.MT_TIMED_OUT
MT_SET_TIMER_FAILED = _RTMA_Definitions2.MT_SET_TIMER_FAILED
class MDF_SET_TIMER_FAILED(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod_id = property(_RTMA_Definitions2.MDF_SET_TIMER_FAILED_mod_id_get, _RTMA_Definitions2.MDF_SET_TIMER_FAILED_mod_id_set)
    timer_id = property(_RTMA_Definitions2.MDF_SET_TIMER_FAILED_timer_id_get, _RTMA_Definitions2.MDF_SET_TIMER_FAILED_timer_id_set)
    snooze_time = property(_RTMA_Definitions2.MDF_SET_TIMER_FAILED_snooze_time_get, _RTMA_Definitions2.MDF_SET_TIMER_FAILED_snooze_time_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_SET_TIMER_FAILED_swiginit(self, _RTMA_Definitions2.new_MDF_SET_TIMER_FAILED())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_SET_TIMER_FAILED

# Register MDF_SET_TIMER_FAILED in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_SET_TIMER_FAILED_swigregister(MDF_SET_TIMER_FAILED)

MT_TM_EXIT = _RTMA_Definitions2.MT_TM_EXIT
MT_SET_TIMER = _RTMA_Definitions2.MT_SET_TIMER
class MDF_SET_TIMER(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    timer_id = property(_RTMA_Definitions2.MDF_SET_TIMER_timer_id_get, _RTMA_Definitions2.MDF_SET_TIMER_timer_id_set)
    snooze_time = property(_RTMA_Definitions2.MDF_SET_TIMER_snooze_time_get, _RTMA_Definitions2.MDF_SET_TIMER_snooze_time_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_SET_TIMER_swiginit(self, _RTMA_Definitions2.new_MDF_SET_TIMER())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_SET_TIMER

# Register MDF_SET_TIMER in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_SET_TIMER_swigregister(MDF_SET_TIMER)

MT_CANCEL_TIMER = _RTMA_Definitions2.MT_CANCEL_TIMER
class MDF_CANCEL_TIMER(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    timer_id = property(_RTMA_Definitions2.MDF_CANCEL_TIMER_timer_id_get, _RTMA_Definitions2.MDF_CANCEL_TIMER_timer_id_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_CANCEL_TIMER_swiginit(self, _RTMA_Definitions2.new_MDF_CANCEL_TIMER())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_CANCEL_TIMER

# Register MDF_CANCEL_TIMER in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_CANCEL_TIMER_swigregister(MDF_CANCEL_TIMER)

MT_LM_EXIT = _RTMA_Definitions2.MT_LM_EXIT
MT_MM_READY = _RTMA_Definitions2.MT_MM_READY
MT_LM_READY = _RTMA_Definitions2.MT_LM_READY
MT_SAVE_MESSAGE_LOG = _RTMA_Definitions2.MT_SAVE_MESSAGE_LOG
MAX_LOGGER_FILENAME_LENGTH = _RTMA_Definitions2.MAX_LOGGER_FILENAME_LENGTH
class MDF_SAVE_MESSAGE_LOG(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    pathname = property(_RTMA_Definitions2.MDF_SAVE_MESSAGE_LOG_pathname_get, _RTMA_Definitions2.MDF_SAVE_MESSAGE_LOG_pathname_set)
    pathname_length = property(_RTMA_Definitions2.MDF_SAVE_MESSAGE_LOG_pathname_length_get, _RTMA_Definitions2.MDF_SAVE_MESSAGE_LOG_pathname_length_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_SAVE_MESSAGE_LOG_swiginit(self, _RTMA_Definitions2.new_MDF_SAVE_MESSAGE_LOG())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_SAVE_MESSAGE_LOG

# Register MDF_SAVE_MESSAGE_LOG in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_SAVE_MESSAGE_LOG_swigregister(MDF_SAVE_MESSAGE_LOG)

MT_MESSAGE_LOG_SAVED = _RTMA_Definitions2.MT_MESSAGE_LOG_SAVED
MT_PAUSE_MESSAGE_LOGGING = _RTMA_Definitions2.MT_PAUSE_MESSAGE_LOGGING
MT_RESUME_MESSAGE_LOGGING = _RTMA_Definitions2.MT_RESUME_MESSAGE_LOGGING
MT_RESET_MESSAGE_LOG = _RTMA_Definitions2.MT_RESET_MESSAGE_LOG
MT_DUMP_MESSAGE_LOG = _RTMA_Definitions2.MT_DUMP_MESSAGE_LOG
MT_TIMING_MESSAGE = _RTMA_Definitions2.MT_TIMING_MESSAGE
class MDF_TIMING_MESSAGE(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    timing = property(_RTMA_Definitions2.MDF_TIMING_MESSAGE_timing_get, _RTMA_Definitions2.MDF_TIMING_MESSAGE_timing_set)
    ModulePID = property(_RTMA_Definitions2.MDF_TIMING_MESSAGE_ModulePID_get, _RTMA_Definitions2.MDF_TIMING_MESSAGE_ModulePID_set)
    send_time = property(_RTMA_Definitions2.MDF_TIMING_MESSAGE_send_time_get, _RTMA_Definitions2.MDF_TIMING_MESSAGE_send_time_set)

    def __init__(self):
        _RTMA_Definitions2.MDF_TIMING_MESSAGE_swiginit(self, _RTMA_Definitions2.new_MDF_TIMING_MESSAGE())
    __swig_destroy__ = _RTMA_Definitions2.delete_MDF_TIMING_MESSAGE

# Register MDF_TIMING_MESSAGE in _RTMA_Definitions2:
_RTMA_Definitions2.MDF_TIMING_MESSAGE_swigregister(MDF_TIMING_MESSAGE)

class DoubleArray(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, nelements):
        _RTMA_Definitions2.DoubleArray_swiginit(self, _RTMA_Definitions2.new_DoubleArray(nelements))
    __swig_destroy__ = _RTMA_Definitions2.delete_DoubleArray

    def __getitem__(self, index):
        return _RTMA_Definitions2.DoubleArray___getitem__(self, index)

    def __setitem__(self, index, value):
        return _RTMA_Definitions2.DoubleArray___setitem__(self, index, value)

    def cast(self):
        return _RTMA_Definitions2.DoubleArray_cast(self)

    @staticmethod
    def frompointer(t):
        return _RTMA_Definitions2.DoubleArray_frompointer(t)

# Register DoubleArray in _RTMA_Definitions2:
_RTMA_Definitions2.DoubleArray_swigregister(DoubleArray)

def DoubleArray_frompointer(t):
    return _RTMA_Definitions2.DoubleArray_frompointer(t)

class UcharArray(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, nelements):
        _RTMA_Definitions2.UcharArray_swiginit(self, _RTMA_Definitions2.new_UcharArray(nelements))
    __swig_destroy__ = _RTMA_Definitions2.delete_UcharArray

    def __getitem__(self, index):
        return _RTMA_Definitions2.UcharArray___getitem__(self, index)

    def __setitem__(self, index, value):
        return _RTMA_Definitions2.UcharArray___setitem__(self, index, value)

    def cast(self):
        return _RTMA_Definitions2.UcharArray_cast(self)

    @staticmethod
    def frompointer(t):
        return _RTMA_Definitions2.UcharArray_frompointer(t)

# Register UcharArray in _RTMA_Definitions2:
_RTMA_Definitions2.UcharArray_swigregister(UcharArray)

def UcharArray_frompointer(t):
    return _RTMA_Definitions2.UcharArray_frompointer(t)




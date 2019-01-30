'''Wrapper for climber_config.h

Generated with:
D:\git\rtma\lang\python\ctypesgen/ctypesgen.py --includedir=D:\git\climber\include -a -o RTMA_config2.py D:\git\climber\include\climber_config.h

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# No libraries

# No modules

MODULE_ID = c_short # d:\\git\\rtma\\include\\rtma_types.h: 6

HOST_ID = c_short # d:\\git\\rtma\\include\\rtma_types.h: 7

MSG_TYPE = c_int # d:\\git\\rtma\\include\\rtma_types.h: 8

MSG_COUNT = c_int # d:\\git\\rtma\\include\\rtma_types.h: 9

# d:\\git\\rtma\\include\\rtma_types.h: 56
class struct_anon_1(Structure):
    pass

struct_anon_1.__slots__ = [
    'msg_type',
    'msg_count',
    'send_time',
    'recv_time',
    'src_host_id',
    'src_mod_id',
    'dest_host_id',
    'dest_mod_id',
    'num_data_bytes',
    'remaining_bytes',
    'is_dynamic',
    'reserved',
]
struct_anon_1._fields_ = [
    ('msg_type', MSG_TYPE),
    ('msg_count', MSG_COUNT),
    ('send_time', c_double),
    ('recv_time', c_double),
    ('src_host_id', HOST_ID),
    ('src_mod_id', MODULE_ID),
    ('dest_host_id', HOST_ID),
    ('dest_mod_id', MODULE_ID),
    ('num_data_bytes', c_int),
    ('remaining_bytes', c_int),
    ('is_dynamic', c_int),
    ('reserved', c_int),
]

RTMA_MSG_HEADER = struct_anon_1 # d:\\git\\rtma\\include\\rtma_types.h: 56

# d:\\git\\rtma\\include\\rtma_types.h: 63
class struct_anon_2(Structure):
    pass

struct_anon_2.__slots__ = [
    'msg_type',
    'msg_count',
    'send_time',
    'recv_time',
    'src_host_id',
    'src_mod_id',
    'dest_host_id',
    'dest_mod_id',
    'num_data_bytes',
    'remaining_bytes',
    'is_dynamic',
    'reserved',
    'data',
]
struct_anon_2._fields_ = [
    ('msg_type', MSG_TYPE),
    ('msg_count', MSG_COUNT),
    ('send_time', c_double),
    ('recv_time', c_double),
    ('src_host_id', HOST_ID),
    ('src_mod_id', MODULE_ID),
    ('dest_host_id', HOST_ID),
    ('dest_mod_id', MODULE_ID),
    ('num_data_bytes', c_int),
    ('remaining_bytes', c_int),
    ('is_dynamic', c_int),
    ('reserved', c_int),
    ('data', c_char * 9000),
]

RTMA_MESSAGE = struct_anon_2 # d:\\git\\rtma\\include\\rtma_types.h: 63

STRING_DATA = POINTER(c_char) # d:\\git\\rtma\\include\\rtma_types.h: 77

# d:\\git\\rtma\\include\\rtma_types.h: 88
class struct_anon_3(Structure):
    pass

struct_anon_3.__slots__ = [
    'mod_id',
    'reserved',
    'msg_type',
]
struct_anon_3._fields_ = [
    ('mod_id', MODULE_ID),
    ('reserved', c_short),
    ('msg_type', MSG_TYPE),
]

MDF_FAIL_SUBSCRIBE = struct_anon_3 # d:\\git\\rtma\\include\\rtma_types.h: 88

# d:\\git\\rtma\\include\\rtma_types.h: 95
class struct_anon_4(Structure):
    pass

struct_anon_4.__slots__ = [
    'dest_mod_id',
    'reserved',
    'time_of_failure',
    'msg_header',
]
struct_anon_4._fields_ = [
    ('dest_mod_id', MODULE_ID),
    ('reserved', c_short * 3),
    ('time_of_failure', c_double),
    ('msg_header', RTMA_MSG_HEADER),
]

MDF_FAILED_MESSAGE = struct_anon_4 # d:\\git\\rtma\\include\\rtma_types.h: 95

MDF_MM_ERROR = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 97

MDF_MM_INFO = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 99

# d:\\git\\rtma\\include\\rtma_types.h: 103
class struct_anon_5(Structure):
    pass

struct_anon_5.__slots__ = [
    'logger_status',
    'daemon_status',
]
struct_anon_5._fields_ = [
    ('logger_status', c_short),
    ('daemon_status', c_short),
]

MDF_CONNECT = struct_anon_5 # d:\\git\\rtma\\include\\rtma_types.h: 103

MDF_SUBSCRIBE = MSG_TYPE # d:\\git\\rtma\\include\\rtma_types.h: 111

MDF_UNSUBSCRIBE = MSG_TYPE # d:\\git\\rtma\\include\\rtma_types.h: 112

MDF_PAUSE_SUBSCRIPTION = MSG_TYPE # d:\\git\\rtma\\include\\rtma_types.h: 113

MDF_RESUME_SUBSCRIPTION = MSG_TYPE # d:\\git\\rtma\\include\\rtma_types.h: 114

# d:\\git\\rtma\\include\\rtma_types.h: 119
class struct_anon_6(Structure):
    pass

struct_anon_6.__slots__ = [
    'mod_id',
]
struct_anon_6._fields_ = [
    ('mod_id', c_int),
]

MDF_FORCE_DISCONNECT = struct_anon_6 # d:\\git\\rtma\\include\\rtma_types.h: 119

# d:\\git\\rtma\\include\\rtma_types.h: 127
class struct_anon_7(Structure):
    pass

struct_anon_7.__slots__ = [
    'pid',
]
struct_anon_7._fields_ = [
    ('pid', c_int),
]

MDF_MODULE_READY = struct_anon_7 # d:\\git\\rtma\\include\\rtma_types.h: 127

MDF_DYNAMIC_DD_READ_ERR = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 129

MDF_DEBUG_TEXT = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 131

MDF_START_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 136

MDF_STOP_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 138

MDF_RESTART_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 140

MDF_KILL_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 142

MDF_SLAVE_START_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 147

# d:\\git\\rtma\\include\\rtma_types.h: 149
class struct_anon_8(Structure):
    pass

struct_anon_8.__slots__ = [
    'num_remote_hosts',
]
struct_anon_8._fields_ = [
    ('num_remote_hosts', c_int),
]

MDF_SLAVE_START_APP_ACK = struct_anon_8 # d:\\git\\rtma\\include\\rtma_types.h: 149

MDF_SLAVE_STOP_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 151

MDF_SLAVE_KILL_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 153

MDF_SLAVE_RESTART_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 155

MDF_AM_ERROR = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 159

MDF_FAIL_START_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 162

MDF_FAIL_STOP_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 164

MDF_FAIL_KILL_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 166

MDF_AM_CONFIG_FILE_DATA = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 174

MDF_AM_APP_NAME = POINTER(c_char) # d:\\git\\rtma\\include\\rtma_types.h: 176

MDF_SLAVE_FAIL_START_APP = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 181

MDF_SLAVE_AM_ERROR = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 188

MDF_APP_ERROR = STRING_DATA # d:\\git\\rtma\\include\\rtma_types.h: 193

# d:\\git\\rtma\\include\\rtma_types.h: 201
class struct_anon_9(Structure):
    pass

struct_anon_9.__slots__ = [
    'timer_id',
]
struct_anon_9._fields_ = [
    ('timer_id', c_int),
]

MDF_TIMER_EXPIRED = struct_anon_9 # d:\\git\\rtma\\include\\rtma_types.h: 201

MDF_TIMED_OUT = MDF_TIMER_EXPIRED # d:\\git\\rtma\\include\\rtma_types.h: 203

# d:\\git\\rtma\\include\\rtma_types.h: 205
class struct_anon_10(Structure):
    pass

struct_anon_10.__slots__ = [
    'mod_id',
    'timer_id',
    'snooze_time',
]
struct_anon_10._fields_ = [
    ('mod_id', MODULE_ID),
    ('timer_id', c_int),
    ('snooze_time', c_int),
]

MDF_SET_TIMER_FAILED = struct_anon_10 # d:\\git\\rtma\\include\\rtma_types.h: 205

# d:\\git\\rtma\\include\\rtma_types.h: 212
class struct_anon_11(Structure):
    pass

struct_anon_11.__slots__ = [
    'timer_id',
    'snooze_time',
]
struct_anon_11._fields_ = [
    ('timer_id', c_int),
    ('snooze_time', c_int),
]

MDF_SET_TIMER = struct_anon_11 # d:\\git\\rtma\\include\\rtma_types.h: 212

# d:\\git\\rtma\\include\\rtma_types.h: 215
class struct_anon_12(Structure):
    pass

struct_anon_12.__slots__ = [
    'timer_id',
]
struct_anon_12._fields_ = [
    ('timer_id', c_int),
]

MDF_CANCEL_TIMER = struct_anon_12 # d:\\git\\rtma\\include\\rtma_types.h: 215

# d:\\git\\rtma\\include\\rtma_types.h: 234
class struct_anon_13(Structure):
    pass

struct_anon_13.__slots__ = [
    'pathname',
    'pathname_length',
]
struct_anon_13._fields_ = [
    ('pathname', c_char * 256),
    ('pathname_length', c_int),
]

MDF_SAVE_MESSAGE_LOG = struct_anon_13 # d:\\git\\rtma\\include\\rtma_types.h: 234

# d:\\git\\rtma\\include\\rtma_types.h: 249
class struct_anon_14(Structure):
    pass

struct_anon_14.__slots__ = [
    'timing',
    'ModulePID',
    'send_time',
]
struct_anon_14._fields_ = [
    ('timing', c_ushort * 10000),
    ('ModulePID', c_int * 200),
    ('send_time', c_double),
]

MDF_TIMING_MESSAGE = struct_anon_14 # d:\\git\\rtma\\include\\rtma_types.h: 249

# D:\\git\\climber\\include\\climber_config.h: 320
class struct_anon_15(Structure):
    pass

struct_anon_15.__slots__ = [
    'serial_no',
    'sub_sample',
]
struct_anon_15._fields_ = [
    ('serial_no', c_int),
    ('sub_sample', c_int),
]

MSG_HEADER = struct_anon_15 # D:\\git\\climber\\include\\climber_config.h: 320

# D:\\git\\climber\\include\\climber_config.h: 329
class struct_anon_16(Structure):
    pass

struct_anon_16.__slots__ = [
    'session_num',
    'set_num',
    'block_num',
    'trial_num',
    'session_type',
    'subject_id',
]
struct_anon_16._fields_ = [
    ('session_num', c_int),
    ('set_num', c_int),
    ('block_num', c_int),
    ('trial_num', c_int),
    ('session_type', c_char * 128),
    ('subject_id', c_char * 64),
]

MDF_TRIAL_METADATA = struct_anon_16 # D:\\git\\climber\\include\\climber_config.h: 329

# D:\\git\\climber\\include\\climber_config.h: 334
class struct_anon_17(Structure):
    pass

struct_anon_17.__slots__ = [
    'rep_num',
    'reserved',
]
struct_anon_17._fields_ = [
    ('rep_num', c_int),
    ('reserved', c_int),
]

MDF_REP_START = struct_anon_17 # D:\\git\\climber\\include\\climber_config.h: 334

# D:\\git\\climber\\include\\climber_config.h: 338
class struct_anon_18(Structure):
    pass

struct_anon_18.__slots__ = [
    'filename',
]
struct_anon_18._fields_ = [
    ('filename', c_char * 256),
]

MDF_PLAYSOUND = struct_anon_18 # D:\\git\\climber\\include\\climber_config.h: 338

# D:\\git\\climber\\include\\climber_config.h: 342
class struct_anon_19(Structure):
    pass

struct_anon_19.__slots__ = [
    'start_command',
]
struct_anon_19._fields_ = [
    ('start_command', c_double),
]

MDF_START_TIMED_RECORDING = struct_anon_19 # D:\\git\\climber\\include\\climber_config.h: 342

# D:\\git\\climber\\include\\climber_config.h: 347
class struct_anon_20(Structure):
    pass

struct_anon_20.__slots__ = [
    'filename',
    'timer',
]
struct_anon_20._fields_ = [
    ('filename', c_char * 256),
    ('timer', c_double),
]

MDF_PICDISPLAY = struct_anon_20 # D:\\git\\climber\\include\\climber_config.h: 347

# D:\\git\\climber\\include\\climber_config.h: 354
class struct_anon_21(Structure):
    pass

struct_anon_21.__slots__ = [
    'ConfigID',
    'Vmax',
    'Vmin',
    'interphase',
]
struct_anon_21._fields_ = [
    ('ConfigID', c_double * 12),
    ('Vmax', c_double * 12),
    ('Vmin', c_double * 12),
    ('interphase', c_double * 12),
]

MDF_STIMDATA = struct_anon_21 # D:\\git\\climber\\include\\climber_config.h: 354

# D:\\git\\climber\\include\\climber_config.h: 367
class struct_anon_22(Structure):
    pass

struct_anon_22.__slots__ = [
    'header',
    'Fx',
    'Fy',
    'Fz',
    'Tz',
    'Tx',
    'Ty',
]
struct_anon_22._fields_ = [
    ('header', MSG_HEADER),
    ('Fx', c_double),
    ('Fy', c_double),
    ('Fz', c_double),
    ('Tz', c_double),
    ('Tx', c_double),
    ('Ty', c_double),
]

MDF_ATIforcesensor = struct_anon_22 # D:\\git\\climber\\include\\climber_config.h: 367

# D:\\git\\climber\\include\\climber_config.h: 374
class struct_anon_23(Structure):
    pass

struct_anon_23.__slots__ = [
    'ardpos',
    'A',
    'B',
    'C',
]
struct_anon_23._fields_ = [
    ('ardpos', c_double * 256),
    ('A', c_double),
    ('B', c_double),
    ('C', c_double),
]

MDF_KNOB_FEEDBACK = struct_anon_23 # D:\\git\\climber\\include\\climber_config.h: 374

# D:\\git\\climber\\include\\climber_config.h: 379
class struct_anon_24(Structure):
    pass

struct_anon_24.__slots__ = [
    'bit',
    'value',
]
struct_anon_24._fields_ = [
    ('bit', c_int),
    ('value', c_int),
]

MDF_SEAIO_OUT = struct_anon_24 # D:\\git\\climber\\include\\climber_config.h: 379

# D:\\git\\climber\\include\\climber_config.h: 385
class struct_anon_25(Structure):
    pass

struct_anon_25.__slots__ = [
    'header',
    'TF',
    'freq',
]
struct_anon_25._fields_ = [
    ('header', MSG_HEADER),
    ('TF', c_double * ((20 * 2) * 128)),
    ('freq', c_double * 20),
]

MDF_TFD = struct_anon_25 # D:\\git\\climber\\include\\climber_config.h: 385

# D:\\git\\climber\\include\\climber_config.h: 391
class struct_anon_26(Structure):
    pass

struct_anon_26.__slots__ = [
    'len',
    'reserved',
    'log',
]
struct_anon_26._fields_ = [
    ('len', c_int),
    ('reserved', c_int),
    ('log', c_char * 512),
]

MDF_HSTLOG = struct_anon_26 # D:\\git\\climber\\include\\climber_config.h: 391

# D:\\git\\climber\\include\\climber_config.h: 397
class struct_anon_27(Structure):
    pass

struct_anon_27.__slots__ = [
    'type',
    'reserved',
    'data',
]
struct_anon_27._fields_ = [
    ('type', c_int),
    ('reserved', c_int),
    ('data', c_char * 256),
]

MDF_EM_CONFIGURATION = struct_anon_27 # D:\\git\\climber\\include\\climber_config.h: 397

# D:\\git\\climber\\include\\climber_config.h: 419
class struct_anon_28(Structure):
    pass

struct_anon_28.__slots__ = [
    'state_name',
    'target',
    'active_assist_weight',
    'brain_control_weight',
    'passive_assist_weight',
    'jstick_control_weight',
    'gain',
    'threshold',
    'force_targ',
    'dZ_gain',
    'force_thresh',
    'active_override',
    'use_for_calib',
    'result_code',
    'stim_enable',
    'force_calib',
    'targ_set',
    'targ_idx',
    'gripperControlMask',
]
struct_anon_28._fields_ = [
    ('state_name', c_char * 128),
    ('target', c_double * 30),
    ('active_assist_weight', c_double * 6),
    ('brain_control_weight', c_double * 6),
    ('passive_assist_weight', c_double * 6),
    ('jstick_control_weight', c_double * 6),
    ('gain', c_double * 6),
    ('threshold', c_double * 6),
    ('force_targ', c_double * 7),
    ('dZ_gain', c_double),
    ('force_thresh', c_double),
    ('active_override', c_int * 30),
    ('use_for_calib', c_int),
    ('result_code', c_int),
    ('stim_enable', c_int),
    ('force_calib', c_int),
    ('targ_set', c_int),
    ('targ_idx', c_int),
    ('gripperControlMask', c_short * 4),
]

MDF_TASK_STATE_CONFIG = struct_anon_28 # D:\\git\\climber\\include\\climber_config.h: 419

# D:\\git\\climber\\include\\climber_config.h: 441
class struct_anon_29(Structure):
    pass

struct_anon_29.__slots__ = [
    'state_name',
    'target',
    'active_assist_weight',
    'brain_control_weight',
    'passive_assist_weight',
    'jstick_control_weight',
    'gain',
    'threshold',
    'force_targ',
    'dZ_gain',
    'force_thresh',
    'active_override',
    'use_for_calib',
    'result_code',
    'stim_enable',
    'force_calib',
    'targ_set',
    'targ_idx',
    'gripperControlMask',
]
struct_anon_29._fields_ = [
    ('state_name', c_char * 128),
    ('target', c_double * 30),
    ('active_assist_weight', c_double * 6),
    ('brain_control_weight', c_double * 6),
    ('passive_assist_weight', c_double * 6),
    ('jstick_control_weight', c_double * 6),
    ('gain', c_double * 6),
    ('threshold', c_double * 6),
    ('force_targ', c_double * 7),
    ('dZ_gain', c_double),
    ('force_thresh', c_double),
    ('active_override', c_int * 30),
    ('use_for_calib', c_int),
    ('result_code', c_int),
    ('stim_enable', c_int),
    ('force_calib', c_int),
    ('targ_set', c_int),
    ('targ_idx', c_int),
    ('gripperControlMask', c_short * 4),
]

MDF_PHASE_RESULT = struct_anon_29 # D:\\git\\climber\\include\\climber_config.h: 441

# D:\\git\\climber\\include\\climber_config.h: 447
class struct_anon_30(Structure):
    pass

struct_anon_30.__slots__ = [
    'src',
    'decoder_type',
    'decoder_loc',
]
struct_anon_30._fields_ = [
    ('src', c_int),
    ('decoder_type', c_char * 128),
    ('decoder_loc', c_char * 256),
]

MDF_EXTRACTION_RESPONSE = struct_anon_30 # D:\\git\\climber\\include\\climber_config.h: 447

# D:\\git\\climber\\include\\climber_config.h: 452
class struct_anon_31(Structure):
    pass

struct_anon_31.__slots__ = [
    'unit_idx',
    'enabled',
]
struct_anon_31._fields_ = [
    ('unit_idx', c_int),
    ('enabled', c_int),
]

MDF_UPDATE_UNIT_STATE = struct_anon_31 # D:\\git\\climber\\include\\climber_config.h: 452

# D:\\git\\climber\\include\\climber_config.h: 457
class struct_anon_32(Structure):
    pass

struct_anon_32.__slots__ = [
    'header',
    'disabled_units',
]
struct_anon_32._fields_ = [
    ('header', MSG_HEADER),
    ('disabled_units', c_ubyte * (2 * (128 * 5))),
]

MDF_DISABLED_UNITS = struct_anon_32 # D:\\git\\climber\\include\\climber_config.h: 457

# D:\\git\\climber\\include\\climber_config.h: 465
class struct_anon_33(Structure):
    pass

struct_anon_33.__slots__ = [
    'header',
    'command',
    'dZ',
    'src',
    'reserved',
]
struct_anon_33._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('dZ', c_double * 7),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_CONTROL_SPACE_COMMAND = struct_anon_33 # D:\\git\\climber\\include\\climber_config.h: 465

# D:\\git\\climber\\include\\climber_config.h: 473
class struct_anon_34(Structure):
    pass

struct_anon_34.__slots__ = [
    'header',
    'command',
    'dZ',
    'src',
    'reserved',
]
struct_anon_34._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('dZ', c_double * 7),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_BIAS_COMMAND = struct_anon_34 # D:\\git\\climber\\include\\climber_config.h: 473

# D:\\git\\climber\\include\\climber_config.h: 480
class struct_anon_35(Structure):
    pass

struct_anon_35.__slots__ = [
    'header',
    'stiffness',
    'src',
    'reserved',
]
struct_anon_35._fields_ = [
    ('header', MSG_HEADER),
    ('stiffness', c_double * 54),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_IMPEDANCE_COMMAND = struct_anon_35 # D:\\git\\climber\\include\\climber_config.h: 480

# D:\\git\\climber\\include\\climber_config.h: 487
class struct_anon_36(Structure):
    pass

struct_anon_36.__slots__ = [
    'header',
    'command',
    'src',
    'reserved',
]
struct_anon_36._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_CONTROL_SPACE_POS_COMMAND = struct_anon_36 # D:\\git\\climber\\include\\climber_config.h: 487

# D:\\git\\climber\\include\\climber_config.h: 495
class struct_anon_37(Structure):
    pass

struct_anon_37.__slots__ = [
    'header',
    'command',
    'stiffness',
    'src',
    'reserved',
]
struct_anon_37._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('stiffness', c_double * 54),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_FINISHED_COMMAND = struct_anon_37 # D:\\git\\climber\\include\\climber_config.h: 495

# D:\\git\\climber\\include\\climber_config.h: 502
class struct_anon_38(Structure):
    pass

struct_anon_38.__slots__ = [
    'header',
    'position',
    'velocity',
]
struct_anon_38._fields_ = [
    ('header', MSG_HEADER),
    ('position', c_double * 30),
    ('velocity', c_double * 30),
]

MDF_CONTROL_SPACE_FEEDBACK = struct_anon_38 # D:\\git\\climber\\include\\climber_config.h: 502

# D:\\git\\climber\\include\\climber_config.h: 510
class struct_anon_39(Structure):
    pass

struct_anon_39.__slots__ = [
    'header',
    'position',
    'velocity',
    'torque',
    'temperature',
]
struct_anon_39._fields_ = [
    ('header', MSG_HEADER),
    ('position', c_double * 54),
    ('velocity', c_double * 54),
    ('torque', c_double * 54),
    ('temperature', c_double * 54),
]

MDF_MPL_RAW_PERCEPT = struct_anon_39 # D:\\git\\climber\\include\\climber_config.h: 510

# D:\\git\\climber\\include\\climber_config.h: 528
class struct_anon_40(Structure):
    pass

struct_anon_40.__slots__ = [
    'header',
    'ind_force',
    'mid_force',
    'rng_force',
    'lit_force',
    'thb_force',
    'ind_accel',
    'mid_accel',
    'rng_accel',
    'lit_accel',
    'thb_accel',
    'contacts',
]
struct_anon_40._fields_ = [
    ('header', MSG_HEADER),
    ('ind_force', c_double * 14),
    ('mid_force', c_double * 14),
    ('rng_force', c_double * 14),
    ('lit_force', c_double * 14),
    ('thb_force', c_double * 14),
    ('ind_accel', c_double * 3),
    ('mid_accel', c_double * 3),
    ('rng_accel', c_double * 3),
    ('lit_accel', c_double * 3),
    ('thb_accel', c_double * 3),
    ('contacts', c_short * 16),
]

MDF_MPL_SEGMENT_PERCEPTS = struct_anon_40 # D:\\git\\climber\\include\\climber_config.h: 528

# D:\\git\\climber\\include\\climber_config.h: 539
class struct_anon_41(Structure):
    pass

struct_anon_41.__slots__ = [
    'header',
    'torque',
    'ind_force',
    'mid_force',
    'rng_force',
    'lit_force',
    'thb_force',
    'contacts',
]
struct_anon_41._fields_ = [
    ('header', MSG_HEADER),
    ('torque', c_double * 54),
    ('ind_force', c_double * 14),
    ('mid_force', c_double * 14),
    ('rng_force', c_double * 14),
    ('lit_force', c_double * 14),
    ('thb_force', c_double * 14),
    ('contacts', c_short * 16),
]

MDF_MPL_REBIASED_SENSORDATA = struct_anon_41 # D:\\git\\climber\\include\\climber_config.h: 539

# D:\\git\\climber\\include\\climber_config.h: 550
class struct_anon_42(Structure):
    pass

struct_anon_42.__slots__ = [
    'header',
    'torque',
    'ind_force',
    'mid_force',
    'rng_force',
    'lit_force',
    'thb_force',
    'contacts',
]
struct_anon_42._fields_ = [
    ('header', MSG_HEADER),
    ('torque', c_double * 54),
    ('ind_force', c_double * 14),
    ('mid_force', c_double * 14),
    ('rng_force', c_double * 14),
    ('lit_force', c_double * 14),
    ('thb_force', c_double * 14),
    ('contacts', c_short * 16),
]

MDF_CURSOR_FEEDBACK = struct_anon_42 # D:\\git\\climber\\include\\climber_config.h: 550

# D:\\git\\climber\\include\\climber_config.h: 555
class struct_anon_43(Structure):
    pass

struct_anon_43.__slots__ = [
    'position',
    'velocity',
]
struct_anon_43._fields_ = [
    ('position', c_double * 7),
    ('velocity', c_double * 7),
]

MDF_WAM_FEEDBACK = struct_anon_43 # D:\\git\\climber\\include\\climber_config.h: 555

# D:\\git\\climber\\include\\climber_config.h: 562
class struct_anon_44(Structure):
    pass

struct_anon_44.__slots__ = [
    'source_index',
    'num_chans_enabled',
    'source_timestamp',
    'data',
]
struct_anon_44._fields_ = [
    ('source_index', c_int),
    ('num_chans_enabled', c_int),
    ('source_timestamp', c_double),
    ('data', c_short * (10 * 128)),
]

MDF_RAW_CTSDATA = struct_anon_44 # D:\\git\\climber\\include\\climber_config.h: 562

# D:\\git\\climber\\include\\climber_config.h: 569
class struct_anon_45(Structure):
    pass

struct_anon_45.__slots__ = [
    'source_index',
    'num_chans_enabled',
    'source_timestamp',
    'data',
]
struct_anon_45._fields_ = [
    ('source_index', c_int),
    ('num_chans_enabled', c_int),
    ('source_timestamp', c_double),
    ('data', c_short * (10 * 16)),
]

MDF_RAW_ANALOGDATA = struct_anon_45 # D:\\git\\climber\\include\\climber_config.h: 569

# D:\\git\\climber\\include\\climber_config.h: 575
class struct_anon_46(Structure):
    pass

struct_anon_46.__slots__ = [
    'header',
    'source_timestamp',
    'data',
]
struct_anon_46._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double * 2),
    ('data', c_short * (((2 * 10) * 2) * 128)),
]

MDF_SPM_CTSDATA = struct_anon_46 # D:\\git\\climber\\include\\climber_config.h: 575

# D:\\git\\climber\\include\\climber_config.h: 581
class struct_anon_47(Structure):
    pass

struct_anon_47.__slots__ = [
    'header',
    'source_timestamp',
    'data',
]
struct_anon_47._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double * 2),
    ('data', c_short * (((2 * 10) * 2) * 16)),
]

MDF_SPM_ANALOGDATA = struct_anon_47 # D:\\git\\climber\\include\\climber_config.h: 581

# D:\\git\\climber\\include\\climber_config.h: 589
class struct_anon_48(Structure):
    pass

struct_anon_48.__slots__ = [
    'source_index',
    'reserved',
    'source_timestamp',
    'count_interval',
    'counts',
]
struct_anon_48._fields_ = [
    ('source_index', c_int),
    ('reserved', c_int),
    ('source_timestamp', c_double),
    ('count_interval', c_double),
    ('counts', c_ubyte * (128 * 5)),
]

MDF_RAW_SPIKECOUNT = struct_anon_48 # D:\\git\\climber\\include\\climber_config.h: 589

SPIKE_COUNT_DATA_TYPE = c_ubyte # D:\\git\\climber\\include\\climber_config.h: 591

# D:\\git\\climber\\include\\climber_config.h: 597
class struct_anon_49(Structure):
    pass

struct_anon_49.__slots__ = [
    'header',
    'source_timestamp',
    'count_interval',
    'counts',
]
struct_anon_49._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double * 2),
    ('count_interval', c_double),
    ('counts', SPIKE_COUNT_DATA_TYPE * (2 * (128 * 5))),
]

MDF_SPM_SPIKECOUNT = struct_anon_49 # D:\\git\\climber\\include\\climber_config.h: 597

# D:\\git\\climber\\include\\climber_config.h: 610
class struct_anon_50(Structure):
    pass

struct_anon_50.__slots__ = [
    'source_index',
    'channel',
    'unit',
    'reserved1',
    'source_timestamp',
    'fPattern',
    'nPeak',
    'nValley',
    'reserved2',
    'snippet',
]
struct_anon_50._fields_ = [
    ('source_index', c_int),
    ('channel', c_short),
    ('unit', c_ubyte),
    ('reserved1', c_ubyte),
    ('source_timestamp', c_double),
    ('fPattern', c_double * 3),
    ('nPeak', c_short),
    ('nValley', c_short),
    ('reserved2', c_int),
    ('snippet', c_short * 48),
]

SPIKE_SNIPPET = struct_anon_50 # D:\\git\\climber\\include\\climber_config.h: 610

# D:\\git\\climber\\include\\climber_config.h: 614
class struct_anon_51(Structure):
    pass

struct_anon_51.__slots__ = [
    'ss',
]
struct_anon_51._fields_ = [
    ('ss', SPIKE_SNIPPET * 25),
]

MDF_SPIKE_SNIPPET = struct_anon_51 # D:\\git\\climber\\include\\climber_config.h: 614

# D:\\git\\climber\\include\\climber_config.h: 628
class struct_anon_52(Structure):
    pass

struct_anon_52.__slots__ = [
    'source_index',
    'channel',
    'unit',
    'reserved1',
    'source_timestamp',
    'fPattern',
    'nPeak',
    'nValley',
    'rejectType',
    'snippet',
]
struct_anon_52._fields_ = [
    ('source_index', c_int),
    ('channel', c_short),
    ('unit', c_ubyte),
    ('reserved1', c_ubyte),
    ('source_timestamp', c_double),
    ('fPattern', c_double * 3),
    ('nPeak', c_short),
    ('nValley', c_short),
    ('rejectType', c_int),
    ('snippet', c_short * 48),
]

REJECTED_SNIPPET = struct_anon_52 # D:\\git\\climber\\include\\climber_config.h: 628

# D:\\git\\climber\\include\\climber_config.h: 632
class struct_anon_53(Structure):
    pass

struct_anon_53.__slots__ = [
    'rs',
]
struct_anon_53._fields_ = [
    ('rs', REJECTED_SNIPPET * 25),
]

MDF_REJECTED_SNIPPET = struct_anon_53 # D:\\git\\climber\\include\\climber_config.h: 632

# D:\\git\\climber\\include\\climber_config.h: 639
class struct_anon_54(Structure):
    pass

struct_anon_54.__slots__ = [
    'source_index',
    'channel',
    'source_timestamp',
    'data',
]
struct_anon_54._fields_ = [
    ('source_index', c_int),
    ('channel', c_int),
    ('source_timestamp', c_double),
    ('data', c_uint * 2),
]

MDF_RAW_DIGITAL_EVENT = struct_anon_54 # D:\\git\\climber\\include\\climber_config.h: 639

# D:\\git\\climber\\include\\climber_config.h: 649
class struct_anon_55(Structure):
    pass

struct_anon_55.__slots__ = [
    'header',
    'source_index',
    'source_timestamp',
    'byte0',
    'byte1',
    'num_events',
    'reserved',
]
struct_anon_55._fields_ = [
    ('header', MSG_HEADER),
    ('source_index', c_int * 10),
    ('source_timestamp', c_double * 2),
    ('byte0', c_ushort * 10),
    ('byte1', c_ushort * 10),
    ('num_events', c_int),
    ('reserved', c_int),
]

MDF_SPM_DIGITAL_EVENT = struct_anon_55 # D:\\git\\climber\\include\\climber_config.h: 649

# D:\\git\\climber\\include\\climber_config.h: 657
class struct_anon_56(Structure):
    pass

struct_anon_56.__slots__ = [
    'source_index',
    'channel',
    'source_timestamp',
    'data',
    'reserved',
]
struct_anon_56._fields_ = [
    ('source_index', c_int),
    ('channel', c_int),
    ('source_timestamp', c_double),
    ('data', c_uint),
    ('reserved', c_int),
]

MDF_STIM_SYNC_EVENT = struct_anon_56 # D:\\git\\climber\\include\\climber_config.h: 657

# D:\\git\\climber\\include\\climber_config.h: 665
class struct_anon_57(Structure):
    pass

struct_anon_57.__slots__ = [
    'source_index',
    'channel',
    'source_timestamp',
    'data',
    'reserved',
]
struct_anon_57._fields_ = [
    ('source_index', c_int),
    ('channel', c_int),
    ('source_timestamp', c_double),
    ('data', c_uint),
    ('reserved', c_int),
]

MDF_STIM_UPDATE_EVENT = struct_anon_57 # D:\\git\\climber\\include\\climber_config.h: 665

# D:\\git\\climber\\include\\climber_config.h: 672
class struct_anon_58(Structure):
    pass

struct_anon_58.__slots__ = [
    'pathname',
    'subjectID',
    'record',
    'reserved',
]
struct_anon_58._fields_ = [
    ('pathname', c_char * 256),
    ('subjectID', c_char * (256 / 2)),
    ('record', c_uint),
    ('reserved', c_uint),
]

MDF_CENTRALRECORD = struct_anon_58 # D:\\git\\climber\\include\\climber_config.h: 672

# D:\\git\\climber\\include\\climber_config.h: 678
class struct_anon_59(Structure):
    pass

struct_anon_59.__slots__ = [
    'header',
    'tag',
    'dof_vals',
]
struct_anon_59._fields_ = [
    ('header', MSG_HEADER),
    ('tag', c_char * 64),
    ('dof_vals', c_double * 30),
]

MDF_INPUT_DOF_DATA = struct_anon_59 # D:\\git\\climber\\include\\climber_config.h: 678

# D:\\git\\climber\\include\\climber_config.h: 689
class struct_anon_60(Structure):
    pass

struct_anon_60.__slots__ = [
    'header',
    'tag',
    'raw_vals',
    'calib_vals',
    'gesture',
    'glovetype',
    'hand',
    'reserved',
]
struct_anon_60._fields_ = [
    ('header', MSG_HEADER),
    ('tag', c_char * 64),
    ('raw_vals', c_double * 18),
    ('calib_vals', c_double * 18),
    ('gesture', c_int),
    ('glovetype', c_int),
    ('hand', c_int),
    ('reserved', c_int),
]

MDF_DATAGLOVE = struct_anon_60 # D:\\git\\climber\\include\\climber_config.h: 689

# D:\\git\\climber\\include\\climber_config.h: 697
class struct_anon_61(Structure):
    pass

struct_anon_61.__slots__ = [
    'header',
    'type',
    'channel',
    'value',
    'time',
]
struct_anon_61._fields_ = [
    ('header', MSG_HEADER),
    ('type', c_int),
    ('channel', c_int),
    ('value', c_int),
    ('time', c_int),
]

MDF_SLIDER_DATA = struct_anon_61 # D:\\git\\climber\\include\\climber_config.h: 697

# D:\\git\\climber\\include\\climber_config.h: 710
class struct_anon_62(Structure):
    pass

struct_anon_62.__slots__ = [
    'configID',
    'amp1',
    'amp2',
    'frequency',
    'num_modules',
    'afcf',
    'width1',
    'width2',
    'interphase',
]
struct_anon_62._fields_ = [
    ('configID', c_int * 16),
    ('amp1', c_int * 16),
    ('amp2', c_int * 16),
    ('frequency', c_int * 16),
    ('num_modules', c_int),
    ('afcf', c_int),
    ('width1', c_int),
    ('width2', c_int),
    ('interphase', c_int),
]

MDF_CERESTIM_CONFIG_MODULE = struct_anon_62 # D:\\git\\climber\\include\\climber_config.h: 710

# D:\\git\\climber\\include\\climber_config.h: 720
class struct_anon_63(Structure):
    pass

struct_anon_63.__slots__ = [
    'header',
    'stop',
    'numChans',
    'channel',
    'pattern',
    'reps',
    'reserved',
]
struct_anon_63._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('numChans', c_int),
    ('channel', c_int * 12),
    ('pattern', c_int * 12),
    ('reps', c_int),
    ('reserved', c_int),
]

MDF_CERESTIM_CONFIG_CHAN = struct_anon_63 # D:\\git\\climber\\include\\climber_config.h: 720

# D:\\git\\climber\\include\\climber_config.h: 735
class struct_anon_64(Structure):
    pass

struct_anon_64.__slots__ = [
    'header',
    'stop',
    'pathname',
    'pathlength',
    'pulselength',
]
struct_anon_64._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('pathname', c_char * 256),
    ('pathlength', c_int),
    ('pulselength', c_int),
]

MDF_CERESTIM_CONFIG_CHAN_ARBITRARY = struct_anon_64 # D:\\git\\climber\\include\\climber_config.h: 735

# D:\\git\\climber\\include\\climber_config.h: 745
class struct_anon_65(Structure):
    pass

struct_anon_65.__slots__ = [
    'header',
    'stop',
    'numChans',
    'channel',
    'pattern',
    'reps',
    'reserved',
]
struct_anon_65._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('numChans', c_int),
    ('channel', c_int * 64),
    ('pattern', c_int * 64),
    ('reps', c_int),
    ('reserved', c_int),
]

MDF_CERESTIM_CONFIG_CHAN_PRESAFETY = struct_anon_65 # D:\\git\\climber\\include\\climber_config.h: 745

# D:\\git\\climber\\include\\climber_config.h: 757
class struct_anon_66(Structure):
    pass

struct_anon_66.__slots__ = [
    'header',
    'stop',
    'numChans',
    'channel',
    'pattern',
    'reps',
    'reserved',
    'pathname',
    'pathlength',
]
struct_anon_66._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('numChans', c_int),
    ('channel', c_int * 64),
    ('pattern', c_int * 64),
    ('reps', c_int),
    ('reserved', c_int),
    ('pathname', c_char * 256),
    ('pathlength', c_int),
]

MDF_CERESTIM_CONFIG_CHAN_PRESAFETY_ARBITRARY = struct_anon_66 # D:\\git\\climber\\include\\climber_config.h: 757

# D:\\git\\climber\\include\\climber_config.h: 763
class struct_anon_67(Structure):
    pass

struct_anon_67.__slots__ = [
    'error',
    'config',
]
struct_anon_67._fields_ = [
    ('error', c_int),
    ('config', c_int),
]

MDF_CERESTIM_ERROR = struct_anon_67 # D:\\git\\climber\\include\\climber_config.h: 763

# D:\\git\\climber\\include\\climber_config.h: 770
class struct_anon_68(Structure):
    pass

struct_anon_68.__slots__ = [
    'pathname',
    'pathname_length',
    'reserved',
]
struct_anon_68._fields_ = [
    ('pathname', c_char * 256),
    ('pathname_length', c_int),
    ('reserved', c_int),
]

MDF_TDMS_CREATE = struct_anon_68 # D:\\git\\climber\\include\\climber_config.h: 770

# D:\\git\\climber\\include\\climber_config.h: 779
class struct_anon_69(Structure):
    pass

struct_anon_69.__slots__ = [
    'handp',
    'handd',
    'head',
    'arms',
    'tag',
    'flipframe',
]
struct_anon_69._fields_ = [
    ('handp', c_char * 48),
    ('handd', c_char * 18),
    ('head', c_char * 13),
    ('arms', c_char * 20),
    ('tag', c_int),
    ('flipframe', c_int),
]

MDF_RF_REPORT = struct_anon_69 # D:\\git\\climber\\include\\climber_config.h: 779

# D:\\git\\climber\\include\\climber_config.h: 785
class struct_anon_70(Structure):
    pass

struct_anon_70.__slots__ = [
    'record',
    'stop',
    'filename',
]
struct_anon_70._fields_ = [
    ('record', c_int),
    ('stop', c_int),
    ('filename', c_char * 256),
]

MDF_AJA_CONFIG = struct_anon_70 # D:\\git\\climber\\include\\climber_config.h: 785

# D:\\git\\climber\\include\\climber_config.h: 790
class struct_anon_71(Structure):
    pass

struct_anon_71.__slots__ = [
    'header',
    'timecode',
]
struct_anon_71._fields_ = [
    ('header', MSG_HEADER),
    ('timecode', c_char * 128),
]

MDF_AJA_TIMECODE = struct_anon_71 # D:\\git\\climber\\include\\climber_config.h: 790

# D:\\git\\climber\\include\\climber_config.h: 796
class struct_anon_72(Structure):
    pass

struct_anon_72.__slots__ = [
    'status',
    'reserved',
    'clipname',
]
struct_anon_72._fields_ = [
    ('status', c_int),
    ('reserved', c_int),
    ('clipname', c_char * 256),
]

MDF_AJA_STATUS = struct_anon_72 # D:\\git\\climber\\include\\climber_config.h: 796

# D:\\git\\climber\\include\\climber_config.h: 802
class struct_anon_73(Structure):
    pass

struct_anon_73.__slots__ = [
    'header',
    'factor',
    'length',
]
struct_anon_73._fields_ = [
    ('header', MSG_HEADER),
    ('factor', c_double),
    ('length', c_double),
]

MDF_NORMALIZATION_FACTOR = struct_anon_73 # D:\\git\\climber\\include\\climber_config.h: 802

# D:\\git\\climber\\include\\climber_config.h: 809
class struct_anon_74(Structure):
    pass

struct_anon_74.__slots__ = [
    'header',
    '_lambda',
    'k',
    'cursor_pos',
]
struct_anon_74._fields_ = [
    ('header', MSG_HEADER),
    ('_lambda', c_float),
    ('k', c_int),
    ('cursor_pos', c_double),
]

MDF_CST_LAMBDA = struct_anon_74 # D:\\git\\climber\\include\\climber_config.h: 809

# D:\\git\\climber\\include\\climber_config.h: 815
class struct_anon_75(Structure):
    pass

struct_anon_75.__slots__ = [
    'sweep_rate',
    'vis_bins',
    'stim_bins',
]
struct_anon_75._fields_ = [
    ('sweep_rate', c_double),
    ('vis_bins', c_int),
    ('stim_bins', c_int),
]

MDF_CST_SETTINGS = struct_anon_75 # D:\\git\\climber\\include\\climber_config.h: 815

# D:\\git\\climber\\include\\climber_config.h: 823
class struct_anon_76(Structure):
    pass

struct_anon_76.__slots__ = [
    'a',
    'reserved',
]
struct_anon_76._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_NATURAL_RESPONSE = struct_anon_76 # D:\\git\\climber\\include\\climber_config.h: 823

# D:\\git\\climber\\include\\climber_config.h: 830
class struct_anon_77(Structure):
    pass

struct_anon_77.__slots__ = [
    'idx',
    'reserved',
]
struct_anon_77._fields_ = [
    ('idx', c_int),
    ('reserved', c_int),
]

MDF_DEPTH_RESPONSE = struct_anon_77 # D:\\git\\climber\\include\\climber_config.h: 830

# D:\\git\\climber\\include\\climber_config.h: 836
class struct_anon_78(Structure):
    pass

struct_anon_78.__slots__ = [
    'a',
    'reserved',
]
struct_anon_78._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_PAIN_RESPONSE = struct_anon_78 # D:\\git\\climber\\include\\climber_config.h: 836

# D:\\git\\climber\\include\\climber_config.h: 842
class struct_anon_79(Structure):
    pass

struct_anon_79.__slots__ = [
    'a',
    'reserved',
]
struct_anon_79._fields_ = [
    ('a', c_int),
    ('reserved', c_int),
]

MDF_MODALITY_TOGGLE = struct_anon_79 # D:\\git\\climber\\include\\climber_config.h: 842

# D:\\git\\climber\\include\\climber_config.h: 848
class struct_anon_80(Structure):
    pass

struct_anon_80.__slots__ = [
    'idx',
    'reserved',
]
struct_anon_80._fields_ = [
    ('idx', c_int),
    ('reserved', c_int),
]

MDF_MECH_RESPONSE = struct_anon_80 # D:\\git\\climber\\include\\climber_config.h: 848

# D:\\git\\climber\\include\\climber_config.h: 854
class struct_anon_81(Structure):
    pass

struct_anon_81.__slots__ = [
    'a',
    'reserved',
]
struct_anon_81._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_MECH_INTENSITY_RESPONSE = struct_anon_81 # D:\\git\\climber\\include\\climber_config.h: 854

# D:\\git\\climber\\include\\climber_config.h: 860
class struct_anon_82(Structure):
    pass

struct_anon_82.__slots__ = [
    'a',
    'reserved',
]
struct_anon_82._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_MOVE_INTENSITY_RESPONSE = struct_anon_82 # D:\\git\\climber\\include\\climber_config.h: 860

# D:\\git\\climber\\include\\climber_config.h: 866
class struct_anon_83(Structure):
    pass

struct_anon_83.__slots__ = [
    'a',
    'reserved',
]
struct_anon_83._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_TINGLE_INTENSITY_RESPONSE = struct_anon_83 # D:\\git\\climber\\include\\climber_config.h: 866

# D:\\git\\climber\\include\\climber_config.h: 872
class struct_anon_84(Structure):
    pass

struct_anon_84.__slots__ = [
    'idx',
    'reserved',
]
struct_anon_84._fields_ = [
    ('idx', c_int),
    ('reserved', c_int),
]

MDF_MOVE_RESPONSE = struct_anon_84 # D:\\git\\climber\\include\\climber_config.h: 872

# D:\\git\\climber\\include\\climber_config.h: 880
class struct_anon_85(Structure):
    pass

struct_anon_85.__slots__ = [
    'img',
    'moreMsgs',
    'reserved',
    'pixels',
]
struct_anon_85._fields_ = [
    ('img', c_char * 32),
    ('moreMsgs', c_int),
    ('reserved', c_int),
    ('pixels', c_float * 64),
]

MDF_DIR_PIXEL_COORDS = struct_anon_85 # D:\\git\\climber\\include\\climber_config.h: 880

# D:\\git\\climber\\include\\climber_config.h: 886
class struct_anon_86(Structure):
    pass

struct_anon_86.__slots__ = [
    'idx',
    'reserved',
]
struct_anon_86._fields_ = [
    ('idx', c_int),
    ('reserved', c_int),
]

MDF_TINGLE_RESPONSE = struct_anon_86 # D:\\git\\climber\\include\\climber_config.h: 886

# D:\\git\\climber\\include\\climber_config.h: 892
class struct_anon_87(Structure):
    pass

struct_anon_87.__slots__ = [
    'a',
    'reserved',
]
struct_anon_87._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_TEMP_RESPONSE = struct_anon_87 # D:\\git\\climber\\include\\climber_config.h: 892

# D:\\git\\climber\\include\\climber_config.h: 900
class struct_anon_88(Structure):
    pass

struct_anon_88.__slots__ = [
    'img',
    'moreMsgs',
    'reserved',
    'pixels',
]
struct_anon_88._fields_ = [
    ('img', c_char * 32),
    ('moreMsgs', c_int),
    ('reserved', c_int),
    ('pixels', c_float * 64),
]

MDF_PIXEL_COORDS = struct_anon_88 # D:\\git\\climber\\include\\climber_config.h: 900

# D:\\git\\climber\\include\\climber_config.h: 909
class struct_anon_89(Structure):
    pass

struct_anon_89.__slots__ = [
    'runindex',
    'serial_no',
    'hour',
    'minute',
    'second',
]
struct_anon_89._fields_ = [
    ('runindex', c_int),
    ('serial_no', c_int),
    ('hour', c_int),
    ('minute', c_int),
    ('second', c_int),
]

MDF_APLC = struct_anon_89 # D:\\git\\climber\\include\\climber_config.h: 909

# D:\\git\\climber\\include\\climber_config.h: 916
class struct_anon_90(Structure):
    pass

struct_anon_90.__slots__ = [
    'filename',
    'randomization',
]
struct_anon_90._fields_ = [
    ('filename', c_char * 256),
    ('randomization', c_int),
]

MDF_STIM_PRES_CONFIG = struct_anon_90 # D:\\git\\climber\\include\\climber_config.h: 916

# D:\\git\\climber\\include\\climber_config.h: 923
class struct_anon_91(Structure):
    pass

struct_anon_91.__slots__ = [
    'stim_filename',
    'stim_state_name',
    'stim_display_time',
    'stim_start_delay',
]
struct_anon_91._fields_ = [
    ('stim_filename', c_char * 256),
    ('stim_state_name', c_char * 256),
    ('stim_display_time', c_double),
    ('stim_start_delay', c_double),
]

MDF_STIM_PRESENT = struct_anon_91 # D:\\git\\climber\\include\\climber_config.h: 923

# D:\\git\\climber\\include\\climber_config.h: 927
class struct_anon_92(Structure):
    pass

struct_anon_92.__slots__ = [
    'phase_rep_end',
]
struct_anon_92._fields_ = [
    ('phase_rep_end', c_int),
]

MDF_STIM_PRES_PHASE_END = struct_anon_92 # D:\\git\\climber\\include\\climber_config.h: 927

# D:\\git\\climber\\include\\climber_config.h: 932
class struct_anon_93(Structure):
    pass

struct_anon_93.__slots__ = [
    'pause_resume',
    'stop',
]
struct_anon_93._fields_ = [
    ('pause_resume', c_int),
    ('stop', c_int),
]

MDF_STIM_PRES_STATUS = struct_anon_93 # D:\\git\\climber\\include\\climber_config.h: 932

# D:\\git\\climber\\include\\climber_config.h: 944
class struct_anon_94(Structure):
    pass

struct_anon_94.__slots__ = [
    'header',
    'grip_pos',
    'velocity',
    'force',
    'impedance',
    'controlMask',
    'src',
    'reserved',
]
struct_anon_94._fields_ = [
    ('header', MSG_HEADER),
    ('grip_pos', c_double * 1),
    ('velocity', c_double * 1),
    ('force', c_double * 1),
    ('impedance', c_double * 1),
    ('controlMask', c_short * 4),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_GRIP_COMMAND = struct_anon_94 # D:\\git\\climber\\include\\climber_config.h: 944

# D:\\git\\climber\\include\\climber_config.h: 954
class struct_anon_95(Structure):
    pass

struct_anon_95.__slots__ = [
    'header',
    'grip_pos',
    'velocity',
    'force',
    'impedance',
    'controlMask',
    'effector',
]
struct_anon_95._fields_ = [
    ('header', MSG_HEADER),
    ('grip_pos', c_double * 1),
    ('velocity', c_double * 1),
    ('force', c_double * 1),
    ('impedance', c_double * 1),
    ('controlMask', c_short * 4),
    ('effector', c_char * 64),
]

MDF_GRIP_FINISHED_COMMAND = struct_anon_95 # D:\\git\\climber\\include\\climber_config.h: 954

# D:\\git\\climber\\include\\climber_config.h: 962
class struct_anon_96(Structure):
    pass

struct_anon_96.__slots__ = [
    'header',
    'grip_pos',
    'velocity',
    'force',
    'effector',
]
struct_anon_96._fields_ = [
    ('header', MSG_HEADER),
    ('grip_pos', c_double * 1),
    ('velocity', c_double * 1),
    ('force', c_double * 2),
    ('effector', c_char * 64),
]

MDF_GRIPPER_FEEDBACK = struct_anon_96 # D:\\git\\climber\\include\\climber_config.h: 962

# D:\\git\\climber\\include\\climber_config.h: 972
class struct_anon_97(Structure):
    pass

struct_anon_97.__slots__ = [
    'header',
    'motor_pos',
    'motor_vel',
    'motor_torque',
    'joint_pos',
    'joint_vel',
    'contact',
]
struct_anon_97._fields_ = [
    ('header', MSG_HEADER),
    ('motor_pos', c_double * 1),
    ('motor_vel', c_double * 1),
    ('motor_torque', c_double * 1),
    ('joint_pos', c_double * 11),
    ('joint_vel', c_double * 11),
    ('contact', c_double * 2),
]

MDF_MUJOCO_SENSOR = struct_anon_97 # D:\\git\\climber\\include\\climber_config.h: 972

# D:\\git\\climber\\include\\climber_config.h: 984
class struct_anon_98(Structure):
    pass

struct_anon_98.__slots__ = [
    'header',
    'ref_pos',
    'ref_vel',
    'gain_pos',
    'gain_vel',
    'ref_pos_enabled',
    'ref_vel_enabled',
    'gain_pos_enabled',
    'gain_vel_enabled',
]
struct_anon_98._fields_ = [
    ('header', MSG_HEADER),
    ('ref_pos', c_double * 1),
    ('ref_vel', c_double * 1),
    ('gain_pos', c_double * 1),
    ('gain_vel', c_double * 1),
    ('ref_pos_enabled', c_short),
    ('ref_vel_enabled', c_short),
    ('gain_pos_enabled', c_short),
    ('gain_vel_enabled', c_short),
]

MDF_MUJOCO_CMD = struct_anon_98 # D:\\git\\climber\\include\\climber_config.h: 984

# D:\\git\\climber\\include\\climber_config.h: 991
class struct_anon_99(Structure):
    pass

struct_anon_99.__slots__ = [
    'mocap_id',
    'link_objects',
    'pos',
]
struct_anon_99._fields_ = [
    ('mocap_id', c_uint),
    ('link_objects', c_uint),
    ('pos', c_double * 3),
]

MDF_MUJOCO_MOVE = struct_anon_99 # D:\\git\\climber\\include\\climber_config.h: 991

# D:\\git\\climber\\include\\climber_config.h: 997
class struct_anon_100(Structure):
    pass

struct_anon_100.__slots__ = [
    'obj_id',
    'pos',
    'orientation',
]
struct_anon_100._fields_ = [
    ('obj_id', c_uint),
    ('pos', c_double * 3),
    ('orientation', c_double * 3),
]

MDF_MUJOCO_OBJMOVE = struct_anon_100 # D:\\git\\climber\\include\\climber_config.h: 997

# D:\\git\\climber\\include\\climber_config.h: 1001
class struct_anon_101(Structure):
    pass

struct_anon_101.__slots__ = [
    'message',
]
struct_anon_101._fields_ = [
    ('message', c_char * 256),
]

MDF_MUJOCO_MSG = struct_anon_101 # D:\\git\\climber\\include\\climber_config.h: 1001

# D:\\git\\climber\\include\\climber_config.h: 1005
class struct_anon_102(Structure):
    pass

struct_anon_102.__slots__ = [
    'color_id',
]
struct_anon_102._fields_ = [
    ('color_id', c_double),
]

MDF_MUJOCO_GHOST_COLOR = struct_anon_102 # D:\\git\\climber\\include\\climber_config.h: 1005

# D:\\git\\climber\\include\\climber_config.h: 1013
class struct_anon_103(Structure):
    pass

struct_anon_103.__slots__ = [
    'header',
    'motor_sp',
    'reserved1',
    'mode',
    'reserved2',
]
struct_anon_103._fields_ = [
    ('header', MSG_HEADER),
    ('motor_sp', c_ushort * 2),
    ('reserved1', c_ushort * 2),
    ('mode', c_ubyte),
    ('reserved2', c_ubyte * 3),
]

MDF_OPENHAND_CMD = struct_anon_103 # D:\\git\\climber\\include\\climber_config.h: 1013

# D:\\git\\climber\\include\\climber_config.h: 1019
class struct_anon_104(Structure):
    pass

struct_anon_104.__slots__ = [
    'header',
    'motor_pos',
    'force',
]
struct_anon_104._fields_ = [
    ('header', MSG_HEADER),
    ('motor_pos', c_ushort),
    ('force', c_ushort),
]

MDF_OPENHAND_SENS = struct_anon_104 # D:\\git\\climber\\include\\climber_config.h: 1019

# D:\\git\\climber\\include\\climber_config.h: 1029
class struct_anon_105(Structure):
    pass

struct_anon_105.__slots__ = [
    'header',
    'ID',
    'reserved',
    'pos',
    'orient',
    'timestamp',
    'name',
]
struct_anon_105._fields_ = [
    ('header', MSG_HEADER),
    ('ID', c_int),
    ('reserved', c_int),
    ('pos', c_double * 3),
    ('orient', c_double * 3),
    ('timestamp', c_double),
    ('name', c_char * 128),
]

MDF_OPTITRACK_RIGID_BODY = struct_anon_105 # D:\\git\\climber\\include\\climber_config.h: 1029

# D:\\git\\climber\\include\\climber_config.h: 1035
class struct_anon_106(Structure):
    pass

struct_anon_106.__slots__ = [
    'header',
    'raw_analog',
    'force',
]
struct_anon_106._fields_ = [
    ('header', MSG_HEADER),
    ('raw_analog', c_int * 3),
    ('force', c_double * 3),
]

MDF_SINGLETACT_DATA = struct_anon_106 # D:\\git\\climber\\include\\climber_config.h: 1035

# D:\\git\\climber\\include\\climber_config.h: 1043
class struct_anon_107(Structure):
    pass

struct_anon_107.__slots__ = [
    'can_id',
    'data',
    'padding',
]
struct_anon_107._fields_ = [
    ('can_id', c_uint),
    ('data', c_ubyte * 8),
    ('padding', c_int),
]

DEKA_CAN_MSG = struct_anon_107 # D:\\git\\climber\\include\\climber_config.h: 1043

# D:\\git\\climber\\include\\climber_config.h: 1051
class struct_anon_108(Structure):
    pass

struct_anon_108.__slots__ = [
    'header',
    'ACI_1',
    'ACI_2',
    'ACI_3',
]
struct_anon_108._fields_ = [
    ('header', MSG_HEADER),
    ('ACI_1', DEKA_CAN_MSG),
    ('ACI_2', DEKA_CAN_MSG),
    ('ACI_3', DEKA_CAN_MSG),
]

MDF_DEKA_ACI_RESPONSE = struct_anon_108 # D:\\git\\climber\\include\\climber_config.h: 1051

# D:\\git\\climber\\include\\climber_config.h: 1064
class struct_anon_109(Structure):
    pass

struct_anon_109.__slots__ = [
    'header',
    'position_msg_1',
    'position_msg_2',
    'motor_pos',
    'motor_current',
    'mode',
    'sync',
    'grip',
    'padding',
]
struct_anon_109._fields_ = [
    ('header', MSG_HEADER),
    ('position_msg_1', DEKA_CAN_MSG),
    ('position_msg_2', DEKA_CAN_MSG),
    ('motor_pos', c_double * 7),
    ('motor_current', c_double * 7),
    ('mode', c_int),
    ('sync', c_int),
    ('grip', c_int),
    ('padding', c_int),
]

MDF_DEKA_SENSOR = struct_anon_109 # D:\\git\\climber\\include\\climber_config.h: 1064

# D:\\git\\climber\\include\\climber_config.h: 1070
class struct_anon_110(Structure):
    pass

struct_anon_110.__slots__ = [
    'toggle',
    'padding',
]
struct_anon_110._fields_ = [
    ('toggle', c_int),
    ('padding', c_int),
]

MDF_DEKA_CAN_TOGGLE = struct_anon_110 # D:\\git\\climber\\include\\climber_config.h: 1070

# D:\\git\\climber\\include\\climber_config.h: 1076
class struct_anon_111(Structure):
    pass

struct_anon_111.__slots__ = [
    'toggle',
    'padding',
]
struct_anon_111._fields_ = [
    ('toggle', c_int),
    ('padding', c_int),
]

MDF_DEKA_CAN_GRIP_TOGGLE = struct_anon_111 # D:\\git\\climber\\include\\climber_config.h: 1076

# D:\\git\\climber\\include\\climber_config.h: 1082
class struct_anon_112(Structure):
    pass

struct_anon_112.__slots__ = [
    'exit',
    'padding',
]
struct_anon_112._fields_ = [
    ('exit', c_int),
    ('padding', c_int),
]

MDF_DEKA_CAN_EXIT = struct_anon_112 # D:\\git\\climber\\include\\climber_config.h: 1082

# D:\\git\\climber\\include\\climber_config.h: 1091
class struct_anon_113(Structure):
    pass

struct_anon_113.__slots__ = [
    'header',
    'joint_dest',
    'err_input_cap',
    'err_cart_wall',
    'err_jpos_stop',
]
struct_anon_113._fields_ = [
    ('header', MSG_HEADER),
    ('joint_dest', c_double * 7),
    ('err_input_cap', c_int * 6),
    ('err_cart_wall', (c_int * 6) * 2),
    ('err_jpos_stop', c_int * 3),
]

MDF_KUKA_JOINT_COMMAND = struct_anon_113 # D:\\git\\climber\\include\\climber_config.h: 1091

# D:\\git\\climber\\include\\climber_config.h: 1106
class struct_anon_114(Structure):
    pass

struct_anon_114.__slots__ = [
    'header',
    'time',
    'joint_pos',
    'cart_pos',
    'cart_angle',
    'cart_pos_vel',
    'cart_rot_vel',
    'cart_force',
    'cart_torque',
    'mode',
    'reserved',
]
struct_anon_114._fields_ = [
    ('header', MSG_HEADER),
    ('time', c_double),
    ('joint_pos', c_double * 7),
    ('cart_pos', c_double * 3),
    ('cart_angle', c_double * 3),
    ('cart_pos_vel', c_double * 3),
    ('cart_rot_vel', c_double * 3),
    ('cart_force', c_double * 3),
    ('cart_torque', c_double * 3),
    ('mode', c_int),
    ('reserved', c_int),
]

MDF_KUKA_FEEDBACK = struct_anon_114 # D:\\git\\climber\\include\\climber_config.h: 1106

# D:\\git\\climber\\include\\climber_config.h: 1112
class struct_anon_115(Structure):
    pass

struct_anon_115.__slots__ = [
    'exit',
    'padding',
]
struct_anon_115._fields_ = [
    ('exit', c_int),
    ('padding', c_int),
]

MDF_KUKA_EXIT = struct_anon_115 # D:\\git\\climber\\include\\climber_config.h: 1112

# D:\\git\\climber\\include\\climber_config.h: 1122
class struct_anon_116(Structure):
    pass

struct_anon_116.__slots__ = [
    'header',
    'num_chans_per_headstage',
    'source_timestamp',
    'data',
]
struct_anon_116._fields_ = [
    ('header', MSG_HEADER),
    ('num_chans_per_headstage', c_int * 2),
    ('source_timestamp', c_uint * 20),
    ('data', c_float * ((20 * 32) * 2)),
]

MDF_XIPP_EMG_DATA_RAW = struct_anon_116 # D:\\git\\climber\\include\\climber_config.h: 1122

# D:\\git\\climber\\include\\climber_config.h: 1129
class struct_anon_117(Structure):
    pass

struct_anon_117.__slots__ = [
    'header',
    'source_timestamp',
    'xipp_timestamp',
    'reserved',
]
struct_anon_117._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double),
    ('xipp_timestamp', c_uint),
    ('reserved', c_int),
]

MDF_SAMPLE_GENERATED = struct_anon_117 # D:\\git\\climber\\include\\climber_config.h: 1129

# D:\\git\\climber\\include\\climber_config.h: 1141
class struct_anon_118(Structure):
    pass

struct_anon_118.__slots__ = [
    'header',
    'stream_type',
    'current',
    'position',
    'external',
    'tension',
    'reserved',
]
struct_anon_118._fields_ = [
    ('header', MSG_HEADER),
    ('stream_type', c_ushort),
    ('current', c_ushort * 5),
    ('position', c_ushort * 5),
    ('external', c_ushort * 7),
    ('tension', c_ushort * 5),
    ('reserved', c_ushort),
]

MDF_PRENSILIA_SENS = struct_anon_118 # D:\\git\\climber\\include\\climber_config.h: 1141

# D:\\git\\climber\\include\\climber_config.h: 1147
class struct_anon_119(Structure):
    pass

struct_anon_119.__slots__ = [
    'header',
    'mode',
    'command',
]
struct_anon_119._fields_ = [
    ('header', MSG_HEADER),
    ('mode', c_ushort * 5),
    ('command', c_ushort * 5),
]

MDF_PRENSILIA_CMD = struct_anon_119 # D:\\git\\climber\\include\\climber_config.h: 1147

# D:\\git\\climber\\include\\climber_config.h: 1165
class struct_anon_120(Structure):
    pass

struct_anon_120.__slots__ = [
    'header',
    'position_msg_1',
    'position_msg_2',
    'force_msg_1',
    'force_msg_2',
    'force_msg_3',
    'motor_pos',
    'contact',
    'mode',
    'status',
    'sync',
    'grip',
]
struct_anon_120._fields_ = [
    ('header', MSG_HEADER),
    ('position_msg_1', DEKA_CAN_MSG),
    ('position_msg_2', DEKA_CAN_MSG),
    ('force_msg_1', DEKA_CAN_MSG),
    ('force_msg_2', DEKA_CAN_MSG),
    ('force_msg_3', DEKA_CAN_MSG),
    ('motor_pos', c_double * 6),
    ('contact', c_double * 13),
    ('mode', c_int),
    ('status', c_int * 13),
    ('sync', c_int),
    ('grip', c_int),
]

MDF_DEKA_HAND_SENSOR = struct_anon_120 # D:\\git\\climber\\include\\climber_config.h: 1165

# D:\\git\\climber\\include\\climber_config.h: 1171
class struct_anon_121(Structure):
    pass

struct_anon_121.__slots__ = [
    'header',
    'ref_vel',
]
struct_anon_121._fields_ = [
    ('header', MSG_HEADER),
    ('ref_vel', c_double * 6),
]

MDF_DEKA_HAND_JSTICK_CMD = struct_anon_121 # D:\\git\\climber\\include\\climber_config.h: 1171

# D:\\git\\climber\\include\\climber_config.h: 1179
class struct_anon_122(Structure):
    pass

struct_anon_122.__slots__ = [
    'proximal_angle',
    'distal_angle',
    'pressure',
    'contact',
]
struct_anon_122._fields_ = [
    ('proximal_angle', c_float),
    ('distal_angle', c_float),
    ('pressure', c_float * 9),
    ('contact', c_int * 9),
]

RH_FINGER_DATA = struct_anon_122 # D:\\git\\climber\\include\\climber_config.h: 1179

# D:\\git\\climber\\include\\climber_config.h: 1189
class struct_anon_123(Structure):
    pass

struct_anon_123.__slots__ = [
    'joint_angle',
    'raw_angle',
    'velocity',
    'load',
    'voltage',
    'temperature',
]
struct_anon_123._fields_ = [
    ('joint_angle', c_float * 4),
    ('raw_angle', c_float * 4),
    ('velocity', c_float * 4),
    ('load', c_float * 4),
    ('voltage', c_float * 4),
    ('temperature', c_int * 4),
]

DYNAMIXEL_INFO = struct_anon_123 # D:\\git\\climber\\include\\climber_config.h: 1189

# D:\\git\\climber\\include\\climber_config.h: 1198
class struct_anon_124(Structure):
    pass

struct_anon_124.__slots__ = [
    'header',
    'finger_1',
    'finger_2',
    'finger_3',
    'motor_info',
]
struct_anon_124._fields_ = [
    ('header', MSG_HEADER),
    ('finger_1', RH_FINGER_DATA),
    ('finger_2', RH_FINGER_DATA),
    ('finger_3', RH_FINGER_DATA),
    ('motor_info', DYNAMIXEL_INFO),
]

MDF_RH_GRIPPER_SENSOR = struct_anon_124 # D:\\git\\climber\\include\\climber_config.h: 1198

# D:\\git\\climber\\include\\climber_config.h: 1209
class struct_anon_125(Structure):
    pass

struct_anon_125.__slots__ = [
    'header',
    'left_plate',
    'left_plate_mean',
    'center_plate',
    'center_plate_mean',
    'right_plate',
    'right_plate_mean',
]
struct_anon_125._fields_ = [
    ('header', MSG_HEADER),
    ('left_plate', c_double * 4),
    ('left_plate_mean', c_double),
    ('center_plate', c_double * 4),
    ('center_plate_mean', c_double),
    ('right_plate', c_double * 4),
    ('right_plate_mean', c_double),
]

MDF_TABLE_LOAD_CELLS = struct_anon_125 # D:\\git\\climber\\include\\climber_config.h: 1209

__const = c_int # <command-line>: 5

# <command-line>: 8
try:
    CTYPESGEN = 1
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 12
try:
    MAX_MODULES = 200
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 13
try:
    DYN_MOD_ID_START = 100
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 14
try:
    MAX_HOSTS = 5
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 15
try:
    MAX_MESSAGE_TYPES = 10000
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 16
try:
    MIN_STREAM_TYPE = 9000
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 17
try:
    MAX_TIMERS = 100
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 18
try:
    MAX_INTERNAL_TIMERS = 20
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 21
try:
    MAX_RTMA_MSG_TYPE = 99
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 22
try:
    MAX_RTMA_MODULE_ID = 9
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 58
try:
    MAX_CONTIGUOUS_MESSAGE_DATA = 9000
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 67
try:
    MID_MESSAGE_MANAGER = 0
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 68
try:
    MID_COMMAND_MODULE = 1
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 69
try:
    MID_APPLICATION_MODULE = 2
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 70
try:
    MID_NETWORK_RELAY = 3
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 71
try:
    MID_STATUS_MODULE = 4
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 72
try:
    MID_QUICKLOGGER = 5
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 74
try:
    HID_LOCAL_HOST = 0
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 75
try:
    HID_ALL_HOSTS = 32767
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 81
try:
    ALL_MESSAGE_TYPES = 2147483647
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 84
try:
    MT_EXIT = 0
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 85
try:
    MT_KILL = 1
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 86
try:
    MT_ACKNOWLEDGE = 2
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 87
try:
    MT_FAIL_SUBSCRIBE = 6
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 89
try:
    MT_FAILED_MESSAGE = 8
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 96
try:
    MT_MM_ERROR = 83
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 98
try:
    MT_MM_INFO = 84
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 102
try:
    MT_CONNECT = 13
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 104
try:
    MT_DISCONNECT = 14
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 107
try:
    MT_SUBSCRIBE = 15
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 108
try:
    MT_UNSUBSCRIBE = 16
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 109
try:
    MT_PAUSE_SUBSCRIPTION = 85
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 110
try:
    MT_RESUME_SUBSCRIPTION = 86
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 116
try:
    MT_SHUTDOWN_RTMA = 17
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 117
try:
    MT_SHUTDOWN_APP = 18
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 118
try:
    MT_FORCE_DISCONNECT = 82
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 123
try:
    MT_CORE_MODULE_REINIT_ACK = 25
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 126
try:
    MT_MODULE_READY = 26
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 128
try:
    MT_DYNAMIC_DD_READ_ERR = 90
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 130
try:
    MT_DEBUG_TEXT = 91
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 134
try:
    MT_AM_EXIT = 30
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 135
try:
    MT_START_APP = 31
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 137
try:
    MT_STOP_APP = 32
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 139
try:
    MT_RESTART_APP = 33
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 141
try:
    MT_KILL_APP = 34
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 143
try:
    MT_AM_RE_READ_CONFIG_FILE = 89
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 144
try:
    MT_AM_GET_APP_NAME = 92
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 146
try:
    MT_SLAVE_START_APP = 64
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 148
try:
    MT_SLAVE_START_APP_ACK = 65
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 150
try:
    MT_SLAVE_STOP_APP = 66
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 152
try:
    MT_SLAVE_KILL_APP = 67
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 154
try:
    MT_SLAVE_RESTART_APP = 68
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 158
try:
    MT_AM_ERROR = 35
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 160
try:
    MT_AM_ACKNOWLEDGE = 36
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 161
try:
    MT_FAIL_START_APP = 37
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 163
try:
    MT_FAIL_STOP_APP = 38
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 165
try:
    MT_FAIL_KILL_APP = 39
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 167
try:
    MT_APP_START_COMPLETE = 40
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 168
try:
    MT_APP_SHUTODWN_COMPLETE = 41
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 169
try:
    MT_APP_RESTART_COMPLETE = 42
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 170
try:
    MT_APP_KILL_COMPLETE = 43
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 171
try:
    MT_ALL_MODULES_READY = 44
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 172
try:
    MT_CORE_MODULE_REINIT = 45
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 173
try:
    MT_AM_CONFIG_FILE_DATA = 46
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 175
try:
    MT_AM_APP_NAME = 93
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 179
try:
    MT_SLAVE_ALL_MODULES_READY = 69
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 180
try:
    MT_SLAVE_FAIL_START_APP = 70
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 182
try:
    MT_SLAVE_FAIL_STOP_APP = 71
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 183
try:
    MT_SLAVE_FAIL_KILL_APP = 72
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 184
try:
    MT_SLAVE_APP_SHUTODWN_COMPLETE = 74
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 185
try:
    MT_SLAVE_APP_RESTART_COMPLETE = 75
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 186
try:
    MT_SLAVE_APP_KILL_COMPLETE = 76
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 187
try:
    MT_SLAVE_AM_ERROR = 77
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 192
try:
    MT_APP_ERROR = 47
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 196
try:
    MT_SM_EXIT = 48
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 199
try:
    MT_CLOCK_SYNC = 49
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 200
try:
    MT_TIMER_EXPIRED = 50
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 202
try:
    MT_TIMED_OUT = 73
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 204
try:
    MT_SET_TIMER_FAILED = 51
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 210
try:
    MT_TM_EXIT = 52
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 211
try:
    MT_SET_TIMER = 53
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 214
try:
    MT_CANCEL_TIMER = 54
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 218
try:
    MT_LM_EXIT = 55
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 221
try:
    MT_MM_READY = 94
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 223
try:
    MT_LM_READY = 96
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 229
try:
    MT_SAVE_MESSAGE_LOG = 56
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 230
try:
    MAX_LOGGER_FILENAME_LENGTH = 256
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 236
try:
    MT_MESSAGE_LOG_SAVED = 57
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 239
try:
    MT_PAUSE_MESSAGE_LOGGING = 58
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 240
try:
    MT_RESUME_MESSAGE_LOGGING = 59
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 241
try:
    MT_RESET_MESSAGE_LOG = 60
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 242
try:
    MT_DUMP_MESSAGE_LOG = 61
except:
    pass

# d:\\git\\rtma\\include\\rtma_types.h: 244
try:
    MT_TIMING_MESSAGE = 80
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 8
try:
    DEFAULT_MM_IP = 'localhost:7111'
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 11
try:
    MAX_SPIKE_SOURCES = 2
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 12
try:
    MAX_SPIKE_CHANS_PER_SOURCE = 128
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 13
try:
    MAX_ANALOG_CHANS = 16
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 14
try:
    MAX_UNITS_PER_CHAN = 5
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 15
try:
    MAX_TOTAL_SPIKE_CHANS_PER_SOURCE = (MAX_SPIKE_CHANS_PER_SOURCE * MAX_UNITS_PER_CHAN)
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 16
try:
    MAX_TOTAL_SPIKE_CHANS = (MAX_SPIKE_SOURCES * MAX_TOTAL_SPIKE_CHANS_PER_SOURCE)
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 17
try:
    LFPSAMPLES_PER_HEARTBEAT = 10
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 18
try:
    ANALOGSAMPLES_PER_HEARTBEAT = 10
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 19
try:
    RAW_COUNTS_PER_SAMPLE = 2
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 20
try:
    SAMPLE_LENGTH = (0.01 * RAW_COUNTS_PER_SAMPLE)
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 21
try:
    SNIPPETS_PER_MESSAGE = 25
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 22
try:
    SAMPLES_PER_SNIPPET = 48
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 23
try:
    MAX_DIG_PER_SAMPLE = 10
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 24
try:
    MAX_DATAGLOVE_SENSORS = 18
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 25
try:
    NUM_DOMAINS = 6
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 26
try:
    MAX_COMMAND_DIMS = 30
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 27
try:
    MPL_RAW_PERCEPT_DIMS = 54
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 29
try:
    NUM_STIM_CHANS = 64
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 30
try:
    SHAM_STIM_CHANS = 32
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 31
try:
    MAX_STIM_CHANS_ON = 12
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 32
try:
    PULSE_TRAIN_SIZE = 101
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 33
try:
    MAX_CS_CONFIGS = 16
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 35
try:
    MAX_XIPP_EEG_HEADSTAGES = 2
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 36
try:
    MAX_XIPP_CHANS = (32 * MAX_XIPP_EEG_HEADSTAGES)
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 37
try:
    MAX_XIPP_ANALOG_CHANS = 32
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 38
try:
    XIPP_SAMPLES_PER_MSG = 20
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 40
try:
    GRIP_DIMS_R = 7
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 41
try:
    GRIP_DIMS_L = 1
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 42
try:
    MAX_GRIP_DIMS = 7
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 43
try:
    MAX_GRIPPER_DIMS = 1
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 44
try:
    MAX_GRIPPER_JOINT_ANGLES = 11
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 45
try:
    MAX_GRIPPER_FORCES = 2
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 46
try:
    MJ_MAX_MOTOR = MAX_GRIPPER_DIMS
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 47
try:
    MJ_MAX_JOINT = MAX_GRIPPER_JOINT_ANGLES
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 48
try:
    MJ_MAX_CONTACT = MAX_GRIPPER_FORCES
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 51
try:
    NoResult = (-1)
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 52
try:
    SuccessfulTrial = 1
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 53
try:
    BadTrial = 2
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 54
try:
    ManualProceed = 4
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 55
try:
    ManualFail = 8
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 58
try:
    HX_DEKA_LUKE_CONTACT_COUNT = 13
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 59
try:
    HX_LUKE_MOTOR_COUNT = 6
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 63
try:
    NUM_FINGERS = 3
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 64
try:
    NUM_SENSORS_PER_FINGER = 9
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 65
try:
    NUM_SENSORS_PALM = 11
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 66
try:
    NUM_TAKKTILE = ((NUM_FINGERS * NUM_SENSORS_PER_FINGER) + NUM_SENSORS_PALM)
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 67
try:
    NUM_ENCODERS = NUM_FINGERS
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 68
try:
    NUM_SERVOS = 4
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 69
try:
    NUM_DYNAMIXEL = NUM_SERVOS
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 74
try:
    MID_JSTICK_COMMAND = 10
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 75
try:
    MID_COMBINER = 11
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 76
try:
    MID_CEREBUS = 12
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 77
try:
    MID_INPUT_TRANSFORM = 20
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 78
try:
    MID_RPPL_RECORD = 21
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 79
try:
    MID_CENTRAL = 22
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 80
try:
    MID_EXTRACTION = 30
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 81
try:
    MID_LFPEXTRACTION = 31
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 82
try:
    MID_CREATEBUFFER = 35
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 83
try:
    MID_MPL_CONTROL = 40
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 84
try:
    MID_GRIP_CONTROL = 41
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 87
try:
    MID_DEKA_CAN_MODULE = 42
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 88
try:
    MID_DEKA_ACI_RESPONSE = 43
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 89
try:
    MID_DEKA_DISPLAY = 47
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 93
try:
    MID_NREC_WAM_RECV = 44
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 94
try:
    MID_NREC_WAM_SEND = 45
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 97
try:
    MID_PSYCHTLBX = 46
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 100
try:
    MID_STIM_PRESENT = 48
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 102
try:
    MID_ACTIVE_ASSIST = 50
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 105
try:
    MID_KUKA_INTERFACE_MODULE = 48
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 106
try:
    MID_KUKA_DISPLAY = 49
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 107
try:
    MID_ROBOTICS_FEEDBACK_INTEGRATOR = 51
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 109
try:
    MID_MPL_FEEDBACK = 60
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 110
try:
    MID_AJA_CONTROL = 65
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 111
try:
    MID_SEAIOCONTROL = 66
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 112
try:
    MID_EXECUTIVE = 70
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 113
try:
    MID_COMMENT_MANAGER = 71
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 114
try:
    MID_StimVoltageMonitor = 77
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 115
try:
    MID_ATIsensor = 78
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 116
try:
    MID_GENERIC = 80
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 117
try:
    MID_MESSAGERATES = 81
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 118
try:
    MID_VISUALIZATION = 82
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 119
try:
    MID_VIDEO_LOGGER = 83
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 120
try:
    MID_AUDIO_LOGGER = 84
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 121
try:
    MID_DATAGLOVE_CONTROL = 85
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 122
try:
    MID_BIASMODULE = 86
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 123
try:
    MID_CURSOR = 87
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 124
try:
    MID_SOUNDPLAYER = 90
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 125
try:
    MID_RFDISPLAY = 91
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 126
try:
    MID_RFACTIVITY = 92
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 127
try:
    MID_ImageDisplayer = 93
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 128
try:
    MID_KNOB_FEEDBACK = 94
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 130
try:
    MID_STIM_SAFETY_MODULE = 95
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 131
try:
    MID_SENSOR_STIM_TRANS_MODULE = 96
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 132
try:
    MID_CERESTIM_CONTROL = 97
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 133
try:
    MID_SENSE_TOUCH_INTERFACE = 98
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 135
try:
    MID_APLSENDER = 98
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 136
try:
    MID_APLRECEIVER = 99
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 139
try:
    MID_RHR_COMMAND_MODULE = 88
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 140
try:
    MID_RHR_SENSOR_MODULE = 89
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 145
try:
    MT_FINISHED_COMMAND = 1700
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 146
try:
    MT_CONTROL_SPACE_FEEDBACK = 1701
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 147
try:
    MT_CONTROL_SPACE_COMMAND = 1702
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 148
try:
    MT_MPL_RAW_PERCEPT = 1703
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 149
try:
    MT_BIAS_COMMAND = 1704
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 150
try:
    MT_MPL_REBIASED_SENSORDATA = 1705
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 151
try:
    MT_CONTROL_SPACE_FEEDBACK_RHR_GRIPPER = 1706
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 152
try:
    MT_CONTROL_SPACE_POS_COMMAND = 1710
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 153
try:
    MT_MPL_SEGMENT_PERCEPTS = 1711
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 154
try:
    MT_WAM_FEEDBACK = 1712
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 155
try:
    MT_IMPEDANCE_COMMAND = 1713
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 156
try:
    MT_CURSOR_FEEDBACK = 1720
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 157
try:
    MT_GRIP_COMMAND = 1730
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 158
try:
    MT_GRIP_FINISHED_COMMAND = 1731
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 159
try:
    MT_GRIPPER_FEEDBACK = 1732
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 160
try:
    MT_MUJOCO_SENSOR = 1733
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 161
try:
    MT_MUJOCO_CMD = 1734
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 162
try:
    MT_MUJOCO_MOVE = 1735
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 163
try:
    MT_MUJOCO_MSG = 1736
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 164
try:
    MT_MUJOCO_GHOST_COLOR = 1737
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 165
try:
    MT_MUJOCO_OBJMOVE = 1738
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 166
try:
    MT_OPENHAND_CMD = 1740
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 167
try:
    MT_OPENHAND_SENS = 1741
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 168
try:
    MT_PRENSILIA_SENS = 1742
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 169
try:
    MT_PRENSILIA_CMD = 1743
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 170
try:
    MT_TABLE_LOAD_CELLS = 1744
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 172
try:
    MT_SINGLETACT_DATA = 1760
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 174
try:
    MT_RAW_SPIKECOUNT = 1800
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 175
try:
    MT_SPM_SPIKECOUNT = 1801
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 176
try:
    MT_SPIKE_SNIPPET = 1802
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 177
try:
    MT_RAW_CTSDATA = 1803
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 178
try:
    MT_SPM_CTSDATA = 1804
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 179
try:
    MT_REJECTED_SNIPPET = 1805
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 180
try:
    MT_RAW_DIGITAL_EVENT = 1806
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 181
try:
    MT_SPM_DIGITAL_EVENT = 1807
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 182
try:
    MT_STIM_SYNC_EVENT = 1808
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 183
try:
    MT_STIM_UPDATE_EVENT = 1809
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 184
try:
    MT_CENTRALRECORD = 1810
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 185
try:
    MT_RAW_ANALOGDATA = 1811
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 186
try:
    MT_SPM_ANALOGDATA = 1812
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 188
try:
    MT_SAMPLE_GENERATED = 1820
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 189
try:
    MT_XIPP_EMG_DATA_RAW = 1830
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 191
try:
    MT_INPUT_DOF_DATA = 1850
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 193
try:
    MT_DATAGLOVE = 1860
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 194
try:
    MT_OPTITRACK_RIGID_BODY = 1861
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 196
try:
    MT_TASK_STATE_CONFIG = 1900
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 197
try:
    MT_PHASE_RESULT = 1901
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 198
try:
    MT_EXTRACTION_RESPONSE = 1902
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 199
try:
    MT_NORMALIZATION_FACTOR = 1903
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 200
try:
    MT_TRIAL_METADATA = 1904
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 201
try:
    MT_EXTRACTION_REQUEST = 1905
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 202
try:
    MT_UPDATE_UNIT_STATE = 1906
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 203
try:
    MT_DISABLED_UNITS = 1907
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 204
try:
    MT_TRIAL_END = 1910
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 205
try:
    MT_REP_START = 1911
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 206
try:
    MT_REP_END = 1912
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 208
try:
    MT_EM_ADAPT_NOW = 2000
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 209
try:
    MT_EM_CONFIGURATION = 2001
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 210
try:
    MT_TDMS_CREATE = 2002
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 211
try:
    MT_RF_REPORT = 2003
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 212
try:
    MT_PICDISPLAY = 2004
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 213
try:
    MT_STIMDATA = 2005
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 214
try:
    MT_KNOB_FEEDBACK = 2006
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 215
try:
    MT_SEAIO_OUT = 2007
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 216
try:
    MT_ATIforcesensor = 2008
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 217
try:
    MT_TACTOR_CMD = 2009
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 218
try:
    MT_HSTLOG = 3000
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 219
try:
    MT_TFD = 3001
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 221
try:
    MT_PLAYSOUND = 3100
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 222
try:
    MT_START_TIMED_RECORDING = 3101
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 224
try:
    MT_AJA_CONFIG = 3200
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 225
try:
    MT_AJA_TIMECODE = 3201
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 226
try:
    MT_AJA_STATUS = 3202
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 227
try:
    MT_AJA_STATUS_REQUEST = 3203
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 230
try:
    MT_APLC = 3500
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 233
try:
    MT_CERESTIM_CONFIG_MODULE = 4000
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 234
try:
    MT_CERESTIM_CONFIG_CHAN_PRESAFETY = 4001
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 235
try:
    MT_CERESTIM_CONFIG_CHAN = 4002
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 236
try:
    MT_CERESTIM_ERROR = 4003
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 237
try:
    MT_CERESTIM_ALIVE = 4004
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 238
try:
    MT_CS_TRAIN_END = 4005
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 239
try:
    MT_CERESTIM_CONFIG_CHAN_PRESAFETY_ARBITRARY = 4006
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 240
try:
    MT_CERESTIM_CONFIG_CHAN_ARBITRARY = 4007
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 241
try:
    MT_CS_ARBITRARY_CLOSE = 4008
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 247
try:
    MT_NATURAL_RESPONSE = 4050
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 248
try:
    MT_DEPTH_RESPONSE = 4051
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 249
try:
    MT_PAIN_RESPONSE = 4052
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 251
try:
    MT_MODALITY_TOGGLE = 4053
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 252
try:
    MT_MECH_RESPONSE = 4054
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 253
try:
    MT_MECH_INTENSITY_RESPONSE = 4055
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 254
try:
    MT_MOVE_RESPONSE = 4056
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 255
try:
    MT_MOVE_INTENSITY_RESPONSE = 4057
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 256
try:
    MT_TINGLE_RESPONSE = 4058
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 257
try:
    MT_TINGLE_INTENSITY_RESPONSE = 4059
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 258
try:
    MT_TEMP_RESPONSE = 4060
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 260
try:
    MT_DIR_PIXEL_COORDS = 4061
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 261
try:
    MT_PIXEL_COORDS = 4063
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 263
try:
    MT_CLEAR_LINE = 4064
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 264
try:
    MT_ADD_SENSATION = 4065
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 266
try:
    MT_SLIDER_DATA = 4066
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 269
try:
    MT_CST_LAMBDA = 4100
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 270
try:
    MT_CST_SETTINGS = 4101
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 273
try:
    MT_STIM_PRES_CONFIG = 4150
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 274
try:
    MT_STIM_PRES_PHASE_END = 4151
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 275
try:
    MT_STIM_PRESENT = 4152
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 276
try:
    MT_STIM_PRES_STATUS = 4153
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 279
try:
    MT_DEKA_ACI_RESPONSE = 4200
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 280
try:
    MT_DEKA_SENSOR = 4201
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 281
try:
    MT_DEKA_CAN_TOGGLE = 4202
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 282
try:
    MT_DEKA_CAN_GRIP_TOGGLE = 4203
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 283
try:
    MT_DEKA_CAN_EXIT = 4204
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 286
try:
    MT_DEKA_HAND_SENSOR = 4205
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 287
try:
    MT_DEKA_HAND_JSTICK_CMD = 4206
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 289
try:
    DEKA_DOF_COUNT = 7
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 292
try:
    MT_RH_GRIPPER_SENSOR = 4207
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 295
try:
    MT_KUKA_JOINT_COMMAND = 4208
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 296
try:
    MT_KUKA_FEEDBACK = 4209
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 297
try:
    MT_KUKA_EXIT = 4210
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 299
try:
    KUKA_DOF_COUNT = 7
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 301
try:
    TAG_LENGTH = 64
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 306
try:
    MPL_AT_ARM_EPV_FING_JV = 0
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 307
try:
    MPL_AT_ARM_EPV_FING_JP = 1
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 308
try:
    MPL_AT_ARM_JV_FING_JP = 2
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 309
try:
    MPL_AT_ALL_JV = 3
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 310
try:
    MPL_AT_ALL_JP = 4
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 311
try:
    MPL_AT_ARM_EPP_FING_JP = 5
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 314
try:
    TFD_FREQ_BINS = 20
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 986
try:
    MUJOCO_LINK_ID = 1000
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 1131
try:
    PRENSILIA_DOF = 5
except:
    pass

# D:\\git\\climber\\include\\climber_config.h: 1132
try:
    PRENSILIA_EXT_SENSORS = 7
except:
    pass

# No inserted files


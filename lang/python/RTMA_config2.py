'''Wrapper for rp3_hst_config.h

Generated with:
C:\hst2\RTMA\lang\python\ctypesgen/ctypesgen.py --includedir=C:\hst2\include -a -o RTMA_config2.py C:\hst2\include\rp3_hst_config.h

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

MODULE_ID = c_short # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 6

HOST_ID = c_short # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 7

MSG_TYPE = c_int # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 8

MSG_COUNT = c_int # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 9

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 56
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

RTMA_MSG_HEADER = struct_anon_1 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 56

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 63
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

RTMA_MESSAGE = struct_anon_2 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 63

STRING_DATA = POINTER(c_char) # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 77

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 88
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

MDF_FAIL_SUBSCRIBE = struct_anon_3 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 88

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 95
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

MDF_FAILED_MESSAGE = struct_anon_4 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 95

MDF_MM_ERROR = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 97

MDF_MM_INFO = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 99

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 103
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

MDF_CONNECT = struct_anon_5 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 103

MDF_SUBSCRIBE = MSG_TYPE # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 111

MDF_UNSUBSCRIBE = MSG_TYPE # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 112

MDF_PAUSE_SUBSCRIPTION = MSG_TYPE # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 113

MDF_RESUME_SUBSCRIPTION = MSG_TYPE # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 114

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 119
class struct_anon_6(Structure):
    pass

struct_anon_6.__slots__ = [
    'mod_id',
]
struct_anon_6._fields_ = [
    ('mod_id', c_int),
]

MDF_FORCE_DISCONNECT = struct_anon_6 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 119

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 127
class struct_anon_7(Structure):
    pass

struct_anon_7.__slots__ = [
    'pid',
]
struct_anon_7._fields_ = [
    ('pid', c_int),
]

MDF_MODULE_READY = struct_anon_7 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 127

MDF_DYNAMIC_DD_READ_ERR = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 129

MDF_DEBUG_TEXT = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 131

MDF_START_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 136

MDF_STOP_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 138

MDF_RESTART_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 140

MDF_KILL_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 142

MDF_SLAVE_START_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 147

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 149
class struct_anon_8(Structure):
    pass

struct_anon_8.__slots__ = [
    'num_remote_hosts',
]
struct_anon_8._fields_ = [
    ('num_remote_hosts', c_int),
]

MDF_SLAVE_START_APP_ACK = struct_anon_8 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 149

MDF_SLAVE_STOP_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 151

MDF_SLAVE_KILL_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 153

MDF_SLAVE_RESTART_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 155

MDF_AM_ERROR = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 159

MDF_FAIL_START_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 162

MDF_FAIL_STOP_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 164

MDF_FAIL_KILL_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 166

MDF_AM_CONFIG_FILE_DATA = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 174

MDF_AM_APP_NAME = POINTER(c_char) # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 176

MDF_SLAVE_FAIL_START_APP = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 181

MDF_SLAVE_AM_ERROR = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 188

MDF_APP_ERROR = STRING_DATA # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 193

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 201
class struct_anon_9(Structure):
    pass

struct_anon_9.__slots__ = [
    'timer_id',
]
struct_anon_9._fields_ = [
    ('timer_id', c_int),
]

MDF_TIMER_EXPIRED = struct_anon_9 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 201

MDF_TIMED_OUT = MDF_TIMER_EXPIRED # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 203

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 205
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

MDF_SET_TIMER_FAILED = struct_anon_10 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 205

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 212
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

MDF_SET_TIMER = struct_anon_11 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 212

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 215
class struct_anon_12(Structure):
    pass

struct_anon_12.__slots__ = [
    'timer_id',
]
struct_anon_12._fields_ = [
    ('timer_id', c_int),
]

MDF_CANCEL_TIMER = struct_anon_12 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 215

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 234
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

MDF_SAVE_MESSAGE_LOG = struct_anon_13 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 234

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 249
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

MDF_TIMING_MESSAGE = struct_anon_14 # C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 249

# C:\\hst2\\include\\rp3_hst_config.h: 200
class struct_anon_15(Structure):
    pass

struct_anon_15.__slots__ = [
    'serial_no',
    'reserved',
]
struct_anon_15._fields_ = [
    ('serial_no', c_int),
    ('reserved', c_int),
]

MSG_HEADER = struct_anon_15 # C:\\hst2\\include\\rp3_hst_config.h: 200

# C:\\hst2\\include\\rp3_hst_config.h: 209
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

MDF_TRIAL_METADATA = struct_anon_16 # C:\\hst2\\include\\rp3_hst_config.h: 209

# C:\\hst2\\include\\rp3_hst_config.h: 214
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

MDF_REP_START = struct_anon_17 # C:\\hst2\\include\\rp3_hst_config.h: 214

# C:\\hst2\\include\\rp3_hst_config.h: 218
class struct_anon_18(Structure):
    pass

struct_anon_18.__slots__ = [
    'filename',
]
struct_anon_18._fields_ = [
    ('filename', c_char * 256),
]

MDF_PLAYSOUND = struct_anon_18 # C:\\hst2\\include\\rp3_hst_config.h: 218

# C:\\hst2\\include\\rp3_hst_config.h: 223
class struct_anon_19(Structure):
    pass

struct_anon_19.__slots__ = [
    'filename',
    'timer',
]
struct_anon_19._fields_ = [
    ('filename', c_char * 256),
    ('timer', c_double),
]

MDF_PICDISPLAY = struct_anon_19 # C:\\hst2\\include\\rp3_hst_config.h: 223

# C:\\hst2\\include\\rp3_hst_config.h: 230
class struct_anon_20(Structure):
    pass

struct_anon_20.__slots__ = [
    'ConfigID',
    'Vmax',
    'Vmin',
    'interphase',
]
struct_anon_20._fields_ = [
    ('ConfigID', c_double * 12),
    ('Vmax', c_double * 12),
    ('Vmin', c_double * 12),
    ('interphase', c_double * 12),
]

MDF_STIMDATA = struct_anon_20 # C:\\hst2\\include\\rp3_hst_config.h: 230

# C:\\hst2\\include\\rp3_hst_config.h: 242
class struct_anon_21(Structure):
    pass

struct_anon_21.__slots__ = [
    'FTsequence',
    'Funits',
    'Tunits',
    'Fx',
    'Fy',
    'Fz',
    'Tz',
    'Tx',
    'Ty',
]
struct_anon_21._fields_ = [
    ('FTsequence', c_int * 2),
    ('Funits', c_char * 128),
    ('Tunits', c_char * 128),
    ('Fx', c_double * 2),
    ('Fy', c_double * 2),
    ('Fz', c_double * 2),
    ('Tz', c_double * 2),
    ('Tx', c_double * 2),
    ('Ty', c_double * 2),
]

MDF_ATIforcesensor = struct_anon_21 # C:\\hst2\\include\\rp3_hst_config.h: 242

# C:\\hst2\\include\\rp3_hst_config.h: 249
class struct_anon_22(Structure):
    pass

struct_anon_22.__slots__ = [
    'ardpos',
    'A',
    'B',
    'C',
]
struct_anon_22._fields_ = [
    ('ardpos', c_double * 256),
    ('A', c_double),
    ('B', c_double),
    ('C', c_double),
]

MDF_KNOB_FEEDBACK = struct_anon_22 # C:\\hst2\\include\\rp3_hst_config.h: 249

# C:\\hst2\\include\\rp3_hst_config.h: 254
class struct_anon_23(Structure):
    pass

struct_anon_23.__slots__ = [
    'bit',
    'value',
]
struct_anon_23._fields_ = [
    ('bit', c_int),
    ('value', c_int),
]

MDF_SEAIO_OUT = struct_anon_23 # C:\\hst2\\include\\rp3_hst_config.h: 254

# C:\\hst2\\include\\rp3_hst_config.h: 260
class struct_anon_24(Structure):
    pass

struct_anon_24.__slots__ = [
    'header',
    'TF',
    'freq',
]
struct_anon_24._fields_ = [
    ('header', MSG_HEADER),
    ('TF', c_double * ((20 * 2) * 128)),
    ('freq', c_double * 20),
]

MDF_TFD = struct_anon_24 # C:\\hst2\\include\\rp3_hst_config.h: 260

# C:\\hst2\\include\\rp3_hst_config.h: 266
class struct_anon_25(Structure):
    pass

struct_anon_25.__slots__ = [
    'len',
    'reserved',
    'log',
]
struct_anon_25._fields_ = [
    ('len', c_int),
    ('reserved', c_int),
    ('log', c_char * 512),
]

MDF_HSTLOG = struct_anon_25 # C:\\hst2\\include\\rp3_hst_config.h: 266

# C:\\hst2\\include\\rp3_hst_config.h: 272
class struct_anon_26(Structure):
    pass

struct_anon_26.__slots__ = [
    'type',
    'reserved',
    'data',
]
struct_anon_26._fields_ = [
    ('type', c_int),
    ('reserved', c_int),
    ('data', c_char * 256),
]

MDF_EM_CONFIGURATION = struct_anon_26 # C:\\hst2\\include\\rp3_hst_config.h: 272

# C:\\hst2\\include\\rp3_hst_config.h: 288
class struct_anon_27(Structure):
    pass

struct_anon_27.__slots__ = [
    'state_name',
    'target',
    'active_assist_weight',
    'brain_control_weight',
    'passive_assist_weight',
    'jstick_control_weight',
    'gain',
    'threshold',
    'active_override',
    'use_for_calib',
    'result_code',
    'stim_enable',
    'reserved',
]
struct_anon_27._fields_ = [
    ('state_name', c_char * 128),
    ('target', c_double * 30),
    ('active_assist_weight', c_double * 6),
    ('brain_control_weight', c_double * 6),
    ('passive_assist_weight', c_double * 6),
    ('jstick_control_weight', c_double * 6),
    ('gain', c_double * 6),
    ('threshold', c_double * 6),
    ('active_override', c_int * 30),
    ('use_for_calib', c_int),
    ('result_code', c_int),
    ('stim_enable', c_int),
    ('reserved', c_int),
]

MDF_TASK_STATE_CONFIG = struct_anon_27 # C:\\hst2\\include\\rp3_hst_config.h: 288

# C:\\hst2\\include\\rp3_hst_config.h: 294
class struct_anon_28(Structure):
    pass

struct_anon_28.__slots__ = [
    'src',
    'decoder_type',
    'decoder_loc',
]
struct_anon_28._fields_ = [
    ('src', c_int),
    ('decoder_type', c_char * 128),
    ('decoder_loc', c_char * 256),
]

MDF_EXTRACTION_RESPONSE = struct_anon_28 # C:\\hst2\\include\\rp3_hst_config.h: 294

# C:\\hst2\\include\\rp3_hst_config.h: 299
class struct_anon_29(Structure):
    pass

struct_anon_29.__slots__ = [
    'unit_idx',
    'enabled',
]
struct_anon_29._fields_ = [
    ('unit_idx', c_int),
    ('enabled', c_int),
]

MDF_UPDATE_UNIT_STATE = struct_anon_29 # C:\\hst2\\include\\rp3_hst_config.h: 299

# C:\\hst2\\include\\rp3_hst_config.h: 304
class struct_anon_30(Structure):
    pass

struct_anon_30.__slots__ = [
    'header',
    'disabled_units',
]
struct_anon_30._fields_ = [
    ('header', MSG_HEADER),
    ('disabled_units', c_ubyte * (2 * (128 * 5))),
]

MDF_DISABLED_UNITS = struct_anon_30 # C:\\hst2\\include\\rp3_hst_config.h: 304

# C:\\hst2\\include\\rp3_hst_config.h: 320
class struct_anon_31(Structure):
    pass

struct_anon_31.__slots__ = [
    'state_name',
    'target',
    'active_assist_weight',
    'brain_control_weight',
    'passive_assist_weight',
    'jstick_control_weight',
    'gain',
    'threshold',
    'active_override',
    'use_for_calib',
    'result_code',
    'stim_enable',
    'reserved',
]
struct_anon_31._fields_ = [
    ('state_name', c_char * 128),
    ('target', c_double * 30),
    ('active_assist_weight', c_double * 6),
    ('brain_control_weight', c_double * 6),
    ('passive_assist_weight', c_double * 6),
    ('jstick_control_weight', c_double * 6),
    ('gain', c_double * 6),
    ('threshold', c_double * 6),
    ('active_override', c_int * 30),
    ('use_for_calib', c_int),
    ('result_code', c_int),
    ('stim_enable', c_int),
    ('reserved', c_int),
]

MDF_PHASE_RESULT = struct_anon_31 # C:\\hst2\\include\\rp3_hst_config.h: 320

# C:\\hst2\\include\\rp3_hst_config.h: 327
class struct_anon_32(Structure):
    pass

struct_anon_32.__slots__ = [
    'header',
    'command',
    'src',
    'reserved',
]
struct_anon_32._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_CONTROL_SPACE_COMMAND = struct_anon_32 # C:\\hst2\\include\\rp3_hst_config.h: 327

# C:\\hst2\\include\\rp3_hst_config.h: 334
class struct_anon_33(Structure):
    pass

struct_anon_33.__slots__ = [
    'header',
    'command',
    'src',
    'reserved',
]
struct_anon_33._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_BIAS_COMMAND = struct_anon_33 # C:\\hst2\\include\\rp3_hst_config.h: 334

# C:\\hst2\\include\\rp3_hst_config.h: 341
class struct_anon_34(Structure):
    pass

struct_anon_34.__slots__ = [
    'header',
    'stiffness',
    'src',
    'reserved',
]
struct_anon_34._fields_ = [
    ('header', MSG_HEADER),
    ('stiffness', c_double * 54),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_IMPEDANCE_COMMAND = struct_anon_34 # C:\\hst2\\include\\rp3_hst_config.h: 341

# C:\\hst2\\include\\rp3_hst_config.h: 348
class struct_anon_35(Structure):
    pass

struct_anon_35.__slots__ = [
    'header',
    'command',
    'src',
    'reserved',
]
struct_anon_35._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_CONTROL_SPACE_POS_COMMAND = struct_anon_35 # C:\\hst2\\include\\rp3_hst_config.h: 348

# C:\\hst2\\include\\rp3_hst_config.h: 356
class struct_anon_36(Structure):
    pass

struct_anon_36.__slots__ = [
    'header',
    'command',
    'stiffness',
    'src',
    'reserved',
]
struct_anon_36._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('stiffness', c_double * 54),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_FINISHED_COMMAND = struct_anon_36 # C:\\hst2\\include\\rp3_hst_config.h: 356

# C:\\hst2\\include\\rp3_hst_config.h: 363
class struct_anon_37(Structure):
    pass

struct_anon_37.__slots__ = [
    'header',
    'position',
    'velocity',
]
struct_anon_37._fields_ = [
    ('header', MSG_HEADER),
    ('position', c_double * 30),
    ('velocity', c_double * 30),
]

MDF_CONTROL_SPACE_FEEDBACK = struct_anon_37 # C:\\hst2\\include\\rp3_hst_config.h: 363

# C:\\hst2\\include\\rp3_hst_config.h: 371
class struct_anon_38(Structure):
    pass

struct_anon_38.__slots__ = [
    'header',
    'position',
    'velocity',
    'torque',
    'temperature',
]
struct_anon_38._fields_ = [
    ('header', MSG_HEADER),
    ('position', c_double * 54),
    ('velocity', c_double * 54),
    ('torque', c_double * 54),
    ('temperature', c_double * 54),
]

MDF_MPL_RAW_PERCEPT = struct_anon_38 # C:\\hst2\\include\\rp3_hst_config.h: 371

# C:\\hst2\\include\\rp3_hst_config.h: 389
class struct_anon_39(Structure):
    pass

struct_anon_39.__slots__ = [
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
struct_anon_39._fields_ = [
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

MDF_MPL_SEGMENT_PERCEPTS = struct_anon_39 # C:\\hst2\\include\\rp3_hst_config.h: 389

# C:\\hst2\\include\\rp3_hst_config.h: 400
class struct_anon_40(Structure):
    pass

struct_anon_40.__slots__ = [
    'header',
    'torque',
    'ind_force',
    'mid_force',
    'rng_force',
    'lit_force',
    'thb_force',
    'contacts',
]
struct_anon_40._fields_ = [
    ('header', MSG_HEADER),
    ('torque', c_double * 54),
    ('ind_force', c_double * 14),
    ('mid_force', c_double * 14),
    ('rng_force', c_double * 14),
    ('lit_force', c_double * 14),
    ('thb_force', c_double * 14),
    ('contacts', c_short * 16),
]

MDF_MPL_REBIASED_SENSORDATA = struct_anon_40 # C:\\hst2\\include\\rp3_hst_config.h: 400

# C:\\hst2\\include\\rp3_hst_config.h: 411
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

MDF_CURSOR_FEEDBACK = struct_anon_41 # C:\\hst2\\include\\rp3_hst_config.h: 411

# C:\\hst2\\include\\rp3_hst_config.h: 416
class struct_anon_42(Structure):
    pass

struct_anon_42.__slots__ = [
    'position',
    'velocity',
]
struct_anon_42._fields_ = [
    ('position', c_double * 7),
    ('velocity', c_double * 7),
]

MDF_WAM_FEEDBACK = struct_anon_42 # C:\\hst2\\include\\rp3_hst_config.h: 416

# C:\\hst2\\include\\rp3_hst_config.h: 423
class struct_anon_43(Structure):
    pass

struct_anon_43.__slots__ = [
    'source_index',
    'reserved',
    'source_timestamp',
    'data',
]
struct_anon_43._fields_ = [
    ('source_index', c_int),
    ('reserved', c_int),
    ('source_timestamp', c_double),
    ('data', c_short * (10 * (128 + 16))),
]

MDF_RAW_CTSDATA = struct_anon_43 # C:\\hst2\\include\\rp3_hst_config.h: 423

# C:\\hst2\\include\\rp3_hst_config.h: 429
class struct_anon_44(Structure):
    pass

struct_anon_44.__slots__ = [
    'header',
    'source_timestamp',
    'data',
]
struct_anon_44._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double * 2),
    ('data', c_short * (((2 * 10) * 2) * (128 + 16))),
]

MDF_SPM_CTSDATA = struct_anon_44 # C:\\hst2\\include\\rp3_hst_config.h: 429

# C:\\hst2\\include\\rp3_hst_config.h: 437
class struct_anon_45(Structure):
    pass

struct_anon_45.__slots__ = [
    'source_index',
    'reserved',
    'source_timestamp',
    'count_interval',
    'counts',
]
struct_anon_45._fields_ = [
    ('source_index', c_int),
    ('reserved', c_int),
    ('source_timestamp', c_double),
    ('count_interval', c_double),
    ('counts', c_ubyte * (128 * 5)),
]

MDF_RAW_SPIKECOUNT = struct_anon_45 # C:\\hst2\\include\\rp3_hst_config.h: 437

SPIKE_COUNT_DATA_TYPE = c_ubyte # C:\\hst2\\include\\rp3_hst_config.h: 439

# C:\\hst2\\include\\rp3_hst_config.h: 445
class struct_anon_46(Structure):
    pass

struct_anon_46.__slots__ = [
    'header',
    'source_timestamp',
    'count_interval',
    'counts',
]
struct_anon_46._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double * 2),
    ('count_interval', c_double),
    ('counts', SPIKE_COUNT_DATA_TYPE * (2 * (128 * 5))),
]

MDF_SPM_SPIKECOUNT = struct_anon_46 # C:\\hst2\\include\\rp3_hst_config.h: 445

# C:\\hst2\\include\\rp3_hst_config.h: 458
class struct_anon_47(Structure):
    pass

struct_anon_47.__slots__ = [
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
struct_anon_47._fields_ = [
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

SPIKE_SNIPPET = struct_anon_47 # C:\\hst2\\include\\rp3_hst_config.h: 458

# C:\\hst2\\include\\rp3_hst_config.h: 462
class struct_anon_48(Structure):
    pass

struct_anon_48.__slots__ = [
    'ss',
]
struct_anon_48._fields_ = [
    ('ss', SPIKE_SNIPPET * 25),
]

MDF_SPIKE_SNIPPET = struct_anon_48 # C:\\hst2\\include\\rp3_hst_config.h: 462

# C:\\hst2\\include\\rp3_hst_config.h: 476
class struct_anon_49(Structure):
    pass

struct_anon_49.__slots__ = [
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
struct_anon_49._fields_ = [
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

REJECTED_SNIPPET = struct_anon_49 # C:\\hst2\\include\\rp3_hst_config.h: 476

# C:\\hst2\\include\\rp3_hst_config.h: 480
class struct_anon_50(Structure):
    pass

struct_anon_50.__slots__ = [
    'rs',
]
struct_anon_50._fields_ = [
    ('rs', REJECTED_SNIPPET * 25),
]

MDF_REJECTED_SNIPPET = struct_anon_50 # C:\\hst2\\include\\rp3_hst_config.h: 480

# C:\\hst2\\include\\rp3_hst_config.h: 487
class struct_anon_51(Structure):
    pass

struct_anon_51.__slots__ = [
    'source_index',
    'channel',
    'source_timestamp',
    'data',
]
struct_anon_51._fields_ = [
    ('source_index', c_int),
    ('channel', c_int),
    ('source_timestamp', c_double),
    ('data', c_uint * 2),
]

MDF_RAW_DIGITAL_EVENT = struct_anon_51 # C:\\hst2\\include\\rp3_hst_config.h: 487

# C:\\hst2\\include\\rp3_hst_config.h: 497
class struct_anon_52(Structure):
    pass

struct_anon_52.__slots__ = [
    'header',
    'source_index',
    'source_timestamp',
    'byte0',
    'byte1',
    'num_events',
    'reserved',
]
struct_anon_52._fields_ = [
    ('header', MSG_HEADER),
    ('source_index', c_int * 10),
    ('source_timestamp', c_double * 2),
    ('byte0', c_ushort * 10),
    ('byte1', c_ushort * 10),
    ('num_events', c_int),
    ('reserved', c_int),
]

MDF_SPM_DIGITAL_EVENT = struct_anon_52 # C:\\hst2\\include\\rp3_hst_config.h: 497

# C:\\hst2\\include\\rp3_hst_config.h: 505
class struct_anon_53(Structure):
    pass

struct_anon_53.__slots__ = [
    'source_index',
    'channel',
    'source_timestamp',
    'data',
    'reserved',
]
struct_anon_53._fields_ = [
    ('source_index', c_int),
    ('channel', c_int),
    ('source_timestamp', c_double),
    ('data', c_uint),
    ('reserved', c_int),
]

MDF_STIM_SYNC_EVENT = struct_anon_53 # C:\\hst2\\include\\rp3_hst_config.h: 505

# C:\\hst2\\include\\rp3_hst_config.h: 513
class struct_anon_54(Structure):
    pass

struct_anon_54.__slots__ = [
    'source_index',
    'channel',
    'source_timestamp',
    'data',
    'reserved',
]
struct_anon_54._fields_ = [
    ('source_index', c_int),
    ('channel', c_int),
    ('source_timestamp', c_double),
    ('data', c_uint),
    ('reserved', c_int),
]

MDF_STIM_UPDATE_EVENT = struct_anon_54 # C:\\hst2\\include\\rp3_hst_config.h: 513

# C:\\hst2\\include\\rp3_hst_config.h: 520
class struct_anon_55(Structure):
    pass

struct_anon_55.__slots__ = [
    'pathname',
    'subjectID',
    'record',
    'reserved',
]
struct_anon_55._fields_ = [
    ('pathname', c_char * 256),
    ('subjectID', c_char * (256 / 2)),
    ('record', c_uint),
    ('reserved', c_uint),
]

MDF_CENTRALRECORD = struct_anon_55 # C:\\hst2\\include\\rp3_hst_config.h: 520

# C:\\hst2\\include\\rp3_hst_config.h: 526
class struct_anon_56(Structure):
    pass

struct_anon_56.__slots__ = [
    'header',
    'tag',
    'dof_vals',
]
struct_anon_56._fields_ = [
    ('header', MSG_HEADER),
    ('tag', c_char * 64),
    ('dof_vals', c_double * 30),
]

MDF_INPUT_DOF_DATA = struct_anon_56 # C:\\hst2\\include\\rp3_hst_config.h: 526

# C:\\hst2\\include\\rp3_hst_config.h: 537
class struct_anon_57(Structure):
    pass

struct_anon_57.__slots__ = [
    'header',
    'tag',
    'raw_vals',
    'calib_vals',
    'gesture',
    'glovetype',
    'hand',
    'reserved',
]
struct_anon_57._fields_ = [
    ('header', MSG_HEADER),
    ('tag', c_char * 64),
    ('raw_vals', c_double * 18),
    ('calib_vals', c_double * 18),
    ('gesture', c_int),
    ('glovetype', c_int),
    ('hand', c_int),
    ('reserved', c_int),
]

MDF_DATAGLOVE = struct_anon_57 # C:\\hst2\\include\\rp3_hst_config.h: 537

# C:\\hst2\\include\\rp3_hst_config.h: 550
class struct_anon_58(Structure):
    pass

struct_anon_58.__slots__ = [
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
struct_anon_58._fields_ = [
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

MDF_CERESTIM_CONFIG_MODULE = struct_anon_58 # C:\\hst2\\include\\rp3_hst_config.h: 550

# C:\\hst2\\include\\rp3_hst_config.h: 560
class struct_anon_59(Structure):
    pass

struct_anon_59.__slots__ = [
    'header',
    'stop',
    'numChans',
    'channel',
    'pattern',
    'reps',
    'reserved',
]
struct_anon_59._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('numChans', c_int),
    ('channel', c_int * 12),
    ('pattern', c_int * 12),
    ('reps', c_int),
    ('reserved', c_int),
]

MDF_CERESTIM_CONFIG_CHAN = struct_anon_59 # C:\\hst2\\include\\rp3_hst_config.h: 560

# C:\\hst2\\include\\rp3_hst_config.h: 570
class struct_anon_60(Structure):
    pass

struct_anon_60.__slots__ = [
    'header',
    'stop',
    'numChans',
    'channel',
    'pattern',
    'reps',
    'reserved',
]
struct_anon_60._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('numChans', c_int),
    ('channel', c_int * 64),
    ('pattern', c_int * 64),
    ('reps', c_int),
    ('reserved', c_int),
]

MDF_CERESTIM_CONFIG_CHAN_PRESAFETY = struct_anon_60 # C:\\hst2\\include\\rp3_hst_config.h: 570

# C:\\hst2\\include\\rp3_hst_config.h: 576
class struct_anon_61(Structure):
    pass

struct_anon_61.__slots__ = [
    'error',
    'config',
]
struct_anon_61._fields_ = [
    ('error', c_int),
    ('config', c_int),
]

MDF_CERESTIM_ERROR = struct_anon_61 # C:\\hst2\\include\\rp3_hst_config.h: 576

# C:\\hst2\\include\\rp3_hst_config.h: 583
class struct_anon_62(Structure):
    pass

struct_anon_62.__slots__ = [
    'pathname',
    'pathname_length',
    'reserved',
]
struct_anon_62._fields_ = [
    ('pathname', c_char * 256),
    ('pathname_length', c_int),
    ('reserved', c_int),
]

MDF_TDMS_CREATE = struct_anon_62 # C:\\hst2\\include\\rp3_hst_config.h: 583

# C:\\hst2\\include\\rp3_hst_config.h: 592
class struct_anon_63(Structure):
    pass

struct_anon_63.__slots__ = [
    'handp',
    'handd',
    'head',
    'arms',
    'tag',
    'flipframe',
]
struct_anon_63._fields_ = [
    ('handp', c_char * 48),
    ('handd', c_char * 18),
    ('head', c_char * 13),
    ('arms', c_char * 20),
    ('tag', c_int),
    ('flipframe', c_int),
]

MDF_RF_REPORT = struct_anon_63 # C:\\hst2\\include\\rp3_hst_config.h: 592

# C:\\hst2\\include\\rp3_hst_config.h: 598
class struct_anon_64(Structure):
    pass

struct_anon_64.__slots__ = [
    'record',
    'stop',
    'filename',
]
struct_anon_64._fields_ = [
    ('record', c_int),
    ('stop', c_int),
    ('filename', c_char * 256),
]

MDF_AJA_CONFIG = struct_anon_64 # C:\\hst2\\include\\rp3_hst_config.h: 598

# C:\\hst2\\include\\rp3_hst_config.h: 603
class struct_anon_65(Structure):
    pass

struct_anon_65.__slots__ = [
    'header',
    'timecode',
]
struct_anon_65._fields_ = [
    ('header', MSG_HEADER),
    ('timecode', c_char * 128),
]

MDF_AJA_TIMECODE = struct_anon_65 # C:\\hst2\\include\\rp3_hst_config.h: 603

# C:\\hst2\\include\\rp3_hst_config.h: 609
class struct_anon_66(Structure):
    pass

struct_anon_66.__slots__ = [
    'status',
    'reserved',
    'clipname',
]
struct_anon_66._fields_ = [
    ('status', c_int),
    ('reserved', c_int),
    ('clipname', c_char * 256),
]

MDF_AJA_STATUS = struct_anon_66 # C:\\hst2\\include\\rp3_hst_config.h: 609

# C:\\hst2\\include\\rp3_hst_config.h: 615
class struct_anon_67(Structure):
    pass

struct_anon_67.__slots__ = [
    'header',
    'factor',
    'length',
]
struct_anon_67._fields_ = [
    ('header', MSG_HEADER),
    ('factor', c_double),
    ('length', c_double),
]

MDF_NORMALIZATION_FACTOR = struct_anon_67 # C:\\hst2\\include\\rp3_hst_config.h: 615

# C:\\hst2\\include\\rp3_hst_config.h: 621
class struct_anon_68(Structure):
    pass

struct_anon_68.__slots__ = [
    'header',
    '_lambda',
    'k',
]
struct_anon_68._fields_ = [
    ('header', MSG_HEADER),
    ('_lambda', c_double),
    ('k', c_double),
]

MDF_CST_LAMBDA = struct_anon_68 # C:\\hst2\\include\\rp3_hst_config.h: 621

# C:\\hst2\\include\\rp3_hst_config.h: 629
class struct_anon_69(Structure):
    pass

struct_anon_69.__slots__ = [
    'a',
    'reserved',
]
struct_anon_69._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_NATURAL_RESPONSE = struct_anon_69 # C:\\hst2\\include\\rp3_hst_config.h: 629

# C:\\hst2\\include\\rp3_hst_config.h: 636
class struct_anon_70(Structure):
    pass

struct_anon_70.__slots__ = [
    'idx',
    'reserved',
]
struct_anon_70._fields_ = [
    ('idx', c_int),
    ('reserved', c_int),
]

MDF_DEPTH_RESPONSE = struct_anon_70 # C:\\hst2\\include\\rp3_hst_config.h: 636

# C:\\hst2\\include\\rp3_hst_config.h: 642
class struct_anon_71(Structure):
    pass

struct_anon_71.__slots__ = [
    'a',
    'reserved',
]
struct_anon_71._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_PAIN_RESPONSE = struct_anon_71 # C:\\hst2\\include\\rp3_hst_config.h: 642

# C:\\hst2\\include\\rp3_hst_config.h: 648
class struct_anon_72(Structure):
    pass

struct_anon_72.__slots__ = [
    'a',
    'reserved',
]
struct_anon_72._fields_ = [
    ('a', c_int),
    ('reserved', c_int),
]

MDF_MODALITY_TOGGLE = struct_anon_72 # C:\\hst2\\include\\rp3_hst_config.h: 648

# C:\\hst2\\include\\rp3_hst_config.h: 654
class struct_anon_73(Structure):
    pass

struct_anon_73.__slots__ = [
    'idx',
    'reserved',
]
struct_anon_73._fields_ = [
    ('idx', c_int),
    ('reserved', c_int),
]

MDF_MECH_RESPONSE = struct_anon_73 # C:\\hst2\\include\\rp3_hst_config.h: 654

# C:\\hst2\\include\\rp3_hst_config.h: 660
class struct_anon_74(Structure):
    pass

struct_anon_74.__slots__ = [
    'a',
    'reserved',
]
struct_anon_74._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_MECH_INTENSITY_RESPONSE = struct_anon_74 # C:\\hst2\\include\\rp3_hst_config.h: 660

# C:\\hst2\\include\\rp3_hst_config.h: 666
class struct_anon_75(Structure):
    pass

struct_anon_75.__slots__ = [
    'a',
    'reserved',
]
struct_anon_75._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_MOVE_INTENSITY_RESPONSE = struct_anon_75 # C:\\hst2\\include\\rp3_hst_config.h: 666

# C:\\hst2\\include\\rp3_hst_config.h: 672
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

MDF_TINGLE_INTENSITY_RESPONSE = struct_anon_76 # C:\\hst2\\include\\rp3_hst_config.h: 672

# C:\\hst2\\include\\rp3_hst_config.h: 678
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

MDF_MOVE_RESPONSE = struct_anon_77 # C:\\hst2\\include\\rp3_hst_config.h: 678

# C:\\hst2\\include\\rp3_hst_config.h: 686
class struct_anon_78(Structure):
    pass

struct_anon_78.__slots__ = [
    'img',
    'moreMsgs',
    'reserved',
    'pixels',
]
struct_anon_78._fields_ = [
    ('img', c_char * 32),
    ('moreMsgs', c_int),
    ('reserved', c_int),
    ('pixels', c_float * 64),
]

MDF_DIR_PIXEL_COORDS = struct_anon_78 # C:\\hst2\\include\\rp3_hst_config.h: 686

# C:\\hst2\\include\\rp3_hst_config.h: 692
class struct_anon_79(Structure):
    pass

struct_anon_79.__slots__ = [
    'idx',
    'reserved',
]
struct_anon_79._fields_ = [
    ('idx', c_int),
    ('reserved', c_int),
]

MDF_TINGLE_RESPONSE = struct_anon_79 # C:\\hst2\\include\\rp3_hst_config.h: 692

# C:\\hst2\\include\\rp3_hst_config.h: 698
class struct_anon_80(Structure):
    pass

struct_anon_80.__slots__ = [
    'a',
    'reserved',
]
struct_anon_80._fields_ = [
    ('a', c_float),
    ('reserved', c_int),
]

MDF_TEMP_RESPONSE = struct_anon_80 # C:\\hst2\\include\\rp3_hst_config.h: 698

# C:\\hst2\\include\\rp3_hst_config.h: 706
class struct_anon_81(Structure):
    pass

struct_anon_81.__slots__ = [
    'img',
    'moreMsgs',
    'reserved',
    'pixels',
]
struct_anon_81._fields_ = [
    ('img', c_char * 32),
    ('moreMsgs', c_int),
    ('reserved', c_int),
    ('pixels', c_float * 64),
]

MDF_PIXEL_COORDS = struct_anon_81 # C:\\hst2\\include\\rp3_hst_config.h: 706

__const = c_int # <command-line>: 5

# <command-line>: 8
try:
    CTYPESGEN = 1
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 12
try:
    MAX_MODULES = 200
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 13
try:
    DYN_MOD_ID_START = 100
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 14
try:
    MAX_HOSTS = 5
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 15
try:
    MAX_MESSAGE_TYPES = 10000
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 16
try:
    MIN_STREAM_TYPE = 9000
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 17
try:
    MAX_TIMERS = 100
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 18
try:
    MAX_INTERNAL_TIMERS = 20
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 21
try:
    MAX_RTMA_MSG_TYPE = 99
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 22
try:
    MAX_RTMA_MODULE_ID = 9
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 58
try:
    MAX_CONTIGUOUS_MESSAGE_DATA = 9000
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 67
try:
    MID_MESSAGE_MANAGER = 0
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 68
try:
    MID_COMMAND_MODULE = 1
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 69
try:
    MID_APPLICATION_MODULE = 2
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 70
try:
    MID_NETWORK_RELAY = 3
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 71
try:
    MID_STATUS_MODULE = 4
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 72
try:
    MID_QUICKLOGGER = 5
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 74
try:
    HID_LOCAL_HOST = 0
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 75
try:
    HID_ALL_HOSTS = 32767
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 81
try:
    ALL_MESSAGE_TYPES = 2147483647
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 84
try:
    MT_EXIT = 0
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 85
try:
    MT_KILL = 1
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 86
try:
    MT_ACKNOWLEDGE = 2
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 87
try:
    MT_FAIL_SUBSCRIBE = 6
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 89
try:
    MT_FAILED_MESSAGE = 8
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 96
try:
    MT_MM_ERROR = 83
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 98
try:
    MT_MM_INFO = 84
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 102
try:
    MT_CONNECT = 13
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 104
try:
    MT_DISCONNECT = 14
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 107
try:
    MT_SUBSCRIBE = 15
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 108
try:
    MT_UNSUBSCRIBE = 16
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 109
try:
    MT_PAUSE_SUBSCRIPTION = 85
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 110
try:
    MT_RESUME_SUBSCRIPTION = 86
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 116
try:
    MT_SHUTDOWN_RTMA = 17
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 117
try:
    MT_SHUTDOWN_APP = 18
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 118
try:
    MT_FORCE_DISCONNECT = 82
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 123
try:
    MT_CORE_MODULE_REINIT_ACK = 25
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 126
try:
    MT_MODULE_READY = 26
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 128
try:
    MT_DYNAMIC_DD_READ_ERR = 90
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 130
try:
    MT_DEBUG_TEXT = 91
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 134
try:
    MT_AM_EXIT = 30
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 135
try:
    MT_START_APP = 31
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 137
try:
    MT_STOP_APP = 32
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 139
try:
    MT_RESTART_APP = 33
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 141
try:
    MT_KILL_APP = 34
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 143
try:
    MT_AM_RE_READ_CONFIG_FILE = 89
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 144
try:
    MT_AM_GET_APP_NAME = 92
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 146
try:
    MT_SLAVE_START_APP = 64
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 148
try:
    MT_SLAVE_START_APP_ACK = 65
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 150
try:
    MT_SLAVE_STOP_APP = 66
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 152
try:
    MT_SLAVE_KILL_APP = 67
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 154
try:
    MT_SLAVE_RESTART_APP = 68
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 158
try:
    MT_AM_ERROR = 35
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 160
try:
    MT_AM_ACKNOWLEDGE = 36
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 161
try:
    MT_FAIL_START_APP = 37
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 163
try:
    MT_FAIL_STOP_APP = 38
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 165
try:
    MT_FAIL_KILL_APP = 39
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 167
try:
    MT_APP_START_COMPLETE = 40
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 168
try:
    MT_APP_SHUTODWN_COMPLETE = 41
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 169
try:
    MT_APP_RESTART_COMPLETE = 42
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 170
try:
    MT_APP_KILL_COMPLETE = 43
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 171
try:
    MT_ALL_MODULES_READY = 44
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 172
try:
    MT_CORE_MODULE_REINIT = 45
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 173
try:
    MT_AM_CONFIG_FILE_DATA = 46
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 175
try:
    MT_AM_APP_NAME = 93
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 179
try:
    MT_SLAVE_ALL_MODULES_READY = 69
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 180
try:
    MT_SLAVE_FAIL_START_APP = 70
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 182
try:
    MT_SLAVE_FAIL_STOP_APP = 71
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 183
try:
    MT_SLAVE_FAIL_KILL_APP = 72
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 184
try:
    MT_SLAVE_APP_SHUTODWN_COMPLETE = 74
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 185
try:
    MT_SLAVE_APP_RESTART_COMPLETE = 75
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 186
try:
    MT_SLAVE_APP_KILL_COMPLETE = 76
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 187
try:
    MT_SLAVE_AM_ERROR = 77
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 192
try:
    MT_APP_ERROR = 47
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 196
try:
    MT_SM_EXIT = 48
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 199
try:
    MT_CLOCK_SYNC = 49
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 200
try:
    MT_TIMER_EXPIRED = 50
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 202
try:
    MT_TIMED_OUT = 73
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 204
try:
    MT_SET_TIMER_FAILED = 51
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 210
try:
    MT_TM_EXIT = 52
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 211
try:
    MT_SET_TIMER = 53
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 214
try:
    MT_CANCEL_TIMER = 54
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 218
try:
    MT_LM_EXIT = 55
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 221
try:
    MT_MM_READY = 94
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 223
try:
    MT_LM_READY = 96
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 229
try:
    MT_SAVE_MESSAGE_LOG = 56
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 230
try:
    MAX_LOGGER_FILENAME_LENGTH = 256
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 236
try:
    MT_MESSAGE_LOG_SAVED = 57
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 239
try:
    MT_PAUSE_MESSAGE_LOGGING = 58
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 240
try:
    MT_RESUME_MESSAGE_LOGGING = 59
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 241
try:
    MT_RESET_MESSAGE_LOG = 60
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 242
try:
    MT_DUMP_MESSAGE_LOG = 61
except:
    pass

# C:\\hst2\\include\\..\\RTMA\\include\\RTMA_types.h: 244
try:
    MT_TIMING_MESSAGE = 80
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 8
try:
    DEFAULT_MM_IP = 'localhost:7111'
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 11
try:
    MAX_SPIKE_SOURCES = 2
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 12
try:
    MAX_SPIKE_CHANS_PER_SOURCE = 128
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 13
try:
    MAX_ANALOG_CHANS = 16
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 14
try:
    MAX_UNITS_PER_CHAN = 5
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 15
try:
    MAX_TOTAL_SPIKE_CHANS_PER_SOURCE = (MAX_SPIKE_CHANS_PER_SOURCE * MAX_UNITS_PER_CHAN)
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 16
try:
    MAX_TOTAL_SPIKE_CHANS = (MAX_SPIKE_SOURCES * MAX_TOTAL_SPIKE_CHANS_PER_SOURCE)
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 17
try:
    LFPSAMPLES_PER_HEARTBEAT = 10
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 18
try:
    RAW_COUNTS_PER_SAMPLE = 2
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 19
try:
    SNIPPETS_PER_MESSAGE = 25
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 20
try:
    SAMPLES_PER_SNIPPET = 48
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 21
try:
    MAX_DIG_PER_SAMPLE = 10
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 22
try:
    MAX_DATAGLOVE_SENSORS = 18
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 23
try:
    NUM_DOMAINS = 6
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 24
try:
    MAX_COMMAND_DIMS = 30
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 25
try:
    MPL_RAW_PERCEPT_DIMS = 54
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 27
try:
    NUM_STIM_CHANS = 64
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 28
try:
    MAX_STIM_CHANS_ON = 12
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 29
try:
    MAX_CS_CONFIGS = 16
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 31
try:
    GRIP_DIMS_R = 1
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 32
try:
    GRIP_DIMS_L = 1
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 35
try:
    NoResult = (-1)
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 36
try:
    SuccessfulTrial = 1
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 37
try:
    BadTrial = 2
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 38
try:
    ManualProceed = 4
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 39
try:
    ManualFail = 8
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 45
try:
    MID_JSTICK_COMMAND = 10
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 46
try:
    MID_COMBINER = 11
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 47
try:
    MID_CEREBUS = 12
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 48
try:
    MID_INPUT_TRANSFORM = 20
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 49
try:
    MID_CENTRAL = 22
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 50
try:
    MID_EXTRACTION = 30
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 51
try:
    MID_LFPEXTRACTION = 31
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 52
try:
    MID_CREATEBUFFER = 35
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 53
try:
    MID_MPL_CONTROL = 40
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 55
try:
    MID_NREC_WAM_RECV = 44
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 56
try:
    MID_NREC_WAM_SEND = 45
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 58
try:
    MID_ACTIVE_ASSIST = 50
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 59
try:
    MID_MPL_FEEDBACK = 60
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 60
try:
    MID_AJA_CONTROL = 65
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 61
try:
    MID_SEAIOCONTROL = 66
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 62
try:
    MID_EXECUTIVE = 70
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 63
try:
    MID_COMMENT_MANAGER = 71
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 64
try:
    MID_StimVoltageMonitor = 77
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 65
try:
    MID_ATIsensor = 78
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 66
try:
    MID_GENERIC = 80
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 67
try:
    MID_MESSAGERATES = 81
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 68
try:
    MID_VISUALIZATION = 82
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 69
try:
    MID_VIDEO_LOGGER = 83
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 70
try:
    MID_AUDIO_LOGGER = 84
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 71
try:
    MID_DATAGLOVE_CONTROL = 85
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 72
try:
    MID_BIASMODULE = 86
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 73
try:
    MID_CURSOR = 87
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 74
try:
    MID_SOUNDPLAYER = 90
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 75
try:
    MID_RFDISPLAY = 91
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 76
try:
    MID_RFACTIVITY = 92
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 77
try:
    MID_ImageDisplayer = 93
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 78
try:
    MID_KNOB_FEEDBACK = 94
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 80
try:
    MID_STIM_SAFETY_MODULE = 95
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 81
try:
    MID_SENSOR_STIM_TRANS_MODULE = 96
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 82
try:
    MID_CERESTIM_CONTROL = 97
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 83
try:
    MID_SENSE_TOUCH_INTERFACE = 98
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 87
try:
    MT_FINISHED_COMMAND = 1700
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 88
try:
    MT_CONTROL_SPACE_FEEDBACK = 1701
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 89
try:
    MT_CONTROL_SPACE_COMMAND = 1702
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 90
try:
    MT_MPL_RAW_PERCEPT = 1703
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 91
try:
    MT_BIAS_COMMAND = 1704
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 92
try:
    MT_MPL_REBIASED_SENSORDATA = 1705
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 93
try:
    MT_CONTROL_SPACE_POS_COMMAND = 1710
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 94
try:
    MT_MPL_SEGMENT_PERCEPTS = 1711
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 95
try:
    MT_WAM_FEEDBACK = 1712
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 96
try:
    MT_IMPEDANCE_COMMAND = 1713
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 97
try:
    MT_CURSOR_FEEDBACK = 1720
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 99
try:
    MT_RAW_SPIKECOUNT = 1800
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 100
try:
    MT_SPM_SPIKECOUNT = 1801
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 101
try:
    MT_SPIKE_SNIPPET = 1802
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 102
try:
    MT_RAW_CTSDATA = 1803
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 103
try:
    MT_SPM_CTSDATA = 1804
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 104
try:
    MT_REJECTED_SNIPPET = 1805
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 105
try:
    MT_RAW_DIGITAL_EVENT = 1806
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 106
try:
    MT_SPM_DIGITAL_EVENT = 1807
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 107
try:
    MT_STIM_SYNC_EVENT = 1808
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 108
try:
    MT_STIM_UPDATE_EVENT = 1809
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 109
try:
    MT_CENTRALRECORD = 1810
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 111
try:
    MT_INPUT_DOF_DATA = 1850
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 113
try:
    MT_DATAGLOVE = 1860
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 115
try:
    MT_TASK_STATE_CONFIG = 1900
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 116
try:
    MT_PHASE_RESULT = 1901
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 117
try:
    MT_EXTRACTION_RESPONSE = 1902
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 118
try:
    MT_NORMALIZATION_FACTOR = 1903
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 119
try:
    MT_TRIAL_METADATA = 1904
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 120
try:
    MT_EXTRACTION_REQUEST = 1905
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 121
try:
    MT_UPDATE_UNIT_STATE = 1906
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 122
try:
    MT_DISABLED_UNITS = 1907
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 123
try:
    MT_TRIAL_END = 1910
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 124
try:
    MT_REP_START = 1911
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 125
try:
    MT_REP_END = 1912
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 128
try:
    MT_EM_ADAPT_NOW = 2000
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 129
try:
    MT_EM_CONFIGURATION = 2001
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 130
try:
    MT_TDMS_CREATE = 2002
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 131
try:
    MT_RF_REPORT = 2003
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 132
try:
    MT_PICDISPLAY = 2004
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 133
try:
    MT_STIMDATA = 2005
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 134
try:
    MT_KNOB_FEEDBACK = 2006
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 135
try:
    MT_SEAIO_OUT = 2007
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 136
try:
    MT_ATIforcesensor = 2008
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 137
try:
    MT_TACTOR_CMD = 2009
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 138
try:
    MT_HSTLOG = 3000
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 139
try:
    MT_TFD = 3001
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 141
try:
    MT_PLAYSOUND = 3100
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 143
try:
    MT_AJA_CONFIG = 3200
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 144
try:
    MT_AJA_TIMECODE = 3201
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 145
try:
    MT_AJA_STATUS = 3202
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 146
try:
    MT_AJA_STATUS_REQUEST = 3203
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 149
try:
    MT_CERESTIM_CONFIG_MODULE = 4000
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 150
try:
    MT_CERESTIM_CONFIG_CHAN_PRESAFETY = 4001
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 151
try:
    MT_CERESTIM_CONFIG_CHAN = 4002
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 152
try:
    MT_CERESTIM_ERROR = 4003
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 153
try:
    MT_CERESTIM_ALIVE = 4004
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 154
try:
    MT_CS_TRAIN_END = 4005
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 159
try:
    MT_NATURAL_RESPONSE = 4050
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 160
try:
    MT_DEPTH_RESPONSE = 4051
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 161
try:
    MT_PAIN_RESPONSE = 4052
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 163
try:
    MT_MODALITY_TOGGLE = 4053
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 164
try:
    MT_MECH_RESPONSE = 4054
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 165
try:
    MT_MECH_INTENSITY_RESPONSE = 4055
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 166
try:
    MT_MOVE_RESPONSE = 4056
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 167
try:
    MT_MOVE_INTENSITY_RESPONSE = 4057
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 168
try:
    MT_TINGLE_RESPONSE = 4058
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 169
try:
    MT_TINGLE_INTENSITY_RESPONSE = 4059
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 170
try:
    MT_TEMP_RESPONSE = 4060
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 172
try:
    MT_DIR_PIXEL_COORDS = 4061
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 173
try:
    MT_PIXEL_COORDS = 4063
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 175
try:
    MT_CLEAR_LINE = 4064
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 176
try:
    MT_ADD_SENSATION = 4065
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 179
try:
    MT_CST_LAMBDA = 4100
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 181
try:
    TAG_LENGTH = 64
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 186
try:
    MPL_AT_ARM_EPV_FING_JV = 0
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 187
try:
    MPL_AT_ARM_EPV_FING_JP = 1
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 188
try:
    MPL_AT_ARM_JV_FING_JP = 2
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 189
try:
    MPL_AT_ALL_JV = 3
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 190
try:
    MPL_AT_ALL_JP = 4
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 191
try:
    MPL_AT_ARM_EPP_FING_JP = 5
except:
    pass

# C:\\hst2\\include\\rp3_hst_config.h: 194
try:
    TFD_FREQ_BINS = 20
except:
    pass

# No inserted files


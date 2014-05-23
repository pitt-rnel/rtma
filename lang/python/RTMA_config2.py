'''Wrapper for rp3_hst_config.h

Generated with:
C:\hst2\RTMA\lang\python\ctypesgen/ctypesgen.py --includedir=C:\hst2\include -a -o RTMA_config2.py C:\hst2\src\Common\include\rp3_hst_config.h

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

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 152
class struct_anon_1(Structure):
    pass

struct_anon_1.__slots__ = [
    'serial_no',
    'reserved',
]
struct_anon_1._fields_ = [
    ('serial_no', c_int),
    ('reserved', c_int),
]

MSG_HEADER = struct_anon_1 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 152

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 156
class struct_anon_2(Structure):
    pass

struct_anon_2.__slots__ = [
    'filename',
]
struct_anon_2._fields_ = [
    ('filename', c_char * 256),
]

MDF_PLAYSOUND = struct_anon_2 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 156

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 161
class struct_anon_3(Structure):
    pass

struct_anon_3.__slots__ = [
    'filename',
    'timer',
]
struct_anon_3._fields_ = [
    ('filename', c_char * 256),
    ('timer', c_double),
]

MDF_PICDISPLAY = struct_anon_3 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 161

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 168
class struct_anon_4(Structure):
    pass

struct_anon_4.__slots__ = [
    'ConfigID',
    'Vmax',
    'Vmin',
    'interphase',
]
struct_anon_4._fields_ = [
    ('ConfigID', c_double * 12),
    ('Vmax', c_double * 12),
    ('Vmin', c_double * 12),
    ('interphase', c_double * 12),
]

MDF_STIMDATA = struct_anon_4 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 168

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 174
class struct_anon_5(Structure):
    pass

struct_anon_5.__slots__ = [
    'header',
    'TF',
    'freq',
]
struct_anon_5._fields_ = [
    ('header', MSG_HEADER),
    ('TF', c_double * ((20 * 2) * 128)),
    ('freq', c_double * 20),
]

MDF_TFD = struct_anon_5 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 174

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 180
class struct_anon_6(Structure):
    pass

struct_anon_6.__slots__ = [
    'len',
    'reserved',
    'log',
]
struct_anon_6._fields_ = [
    ('len', c_int),
    ('reserved', c_int),
    ('log', c_char * 512),
]

MDF_HSTLOG = struct_anon_6 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 180

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 186
class struct_anon_7(Structure):
    pass

struct_anon_7.__slots__ = [
    'type',
    'reserved',
    'data',
]
struct_anon_7._fields_ = [
    ('type', c_int),
    ('reserved', c_int),
    ('data', c_char * 256),
]

MDF_EM_CONFIGURATION = struct_anon_7 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 186

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 200
class struct_anon_8(Structure):
    pass

struct_anon_8.__slots__ = [
    'state_name',
    'target',
    'active_assist_weight',
    'brain_control_weight',
    'passive_assist_weight',
    'jstick_control_weight',
    'gain',
    'use_for_calib',
    'result_code',
    'stim_enable',
    'reserved',
]
struct_anon_8._fields_ = [
    ('state_name', c_char * 128),
    ('target', c_double * 30),
    ('active_assist_weight', c_double * 6),
    ('brain_control_weight', c_double * 6),
    ('passive_assist_weight', c_double * 6),
    ('jstick_control_weight', c_double * 6),
    ('gain', c_double * 6),
    ('use_for_calib', c_int),
    ('result_code', c_int),
    ('stim_enable', c_int),
    ('reserved', c_int),
]

MDF_TASK_STATE_CONFIG = struct_anon_8 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 200

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 206
class struct_anon_9(Structure):
    pass

struct_anon_9.__slots__ = [
    'src',
    'decoder_type',
    'decoder_loc',
]
struct_anon_9._fields_ = [
    ('src', c_int),
    ('decoder_type', c_char * 128),
    ('decoder_loc', c_char * 256),
]

MDF_EXTRACTION_RESPONSE = struct_anon_9 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 206

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 220
class struct_anon_10(Structure):
    pass

struct_anon_10.__slots__ = [
    'state_name',
    'target',
    'active_assist_weight',
    'brain_control_weight',
    'passive_assist_weight',
    'jstick_control_weight',
    'gain',
    'use_for_calib',
    'result_code',
    'stim_enable',
    'reserved',
]
struct_anon_10._fields_ = [
    ('state_name', c_char * 128),
    ('target', c_double * 30),
    ('active_assist_weight', c_double * 6),
    ('brain_control_weight', c_double * 6),
    ('passive_assist_weight', c_double * 6),
    ('jstick_control_weight', c_double * 6),
    ('gain', c_double * 6),
    ('use_for_calib', c_int),
    ('result_code', c_int),
    ('stim_enable', c_int),
    ('reserved', c_int),
]

MDF_PHASE_RESULT = struct_anon_10 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 220

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 227
class struct_anon_11(Structure):
    pass

struct_anon_11.__slots__ = [
    'header',
    'command',
    'src',
    'reserved',
]
struct_anon_11._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_CONTROL_SPACE_COMMAND = struct_anon_11 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 227

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 234
class struct_anon_12(Structure):
    pass

struct_anon_12.__slots__ = [
    'header',
    'command',
    'src',
    'reserved',
]
struct_anon_12._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_CONTROL_SPACE_POS_COMMAND = struct_anon_12 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 234

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 241
class struct_anon_13(Structure):
    pass

struct_anon_13.__slots__ = [
    'header',
    'command',
    'src',
    'reserved',
]
struct_anon_13._fields_ = [
    ('header', MSG_HEADER),
    ('command', c_double * 30),
    ('src', c_int),
    ('reserved', c_int),
]

MDF_FINISHED_COMMAND = struct_anon_13 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 241

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 248
class struct_anon_14(Structure):
    pass

struct_anon_14.__slots__ = [
    'header',
    'position',
    'velocity',
]
struct_anon_14._fields_ = [
    ('header', MSG_HEADER),
    ('position', c_double * 30),
    ('velocity', c_double * 30),
]

MDF_CONTROL_SPACE_FEEDBACK = struct_anon_14 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 248

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 256
class struct_anon_15(Structure):
    pass

struct_anon_15.__slots__ = [
    'header',
    'position',
    'velocity',
    'torque',
    'temperature',
]
struct_anon_15._fields_ = [
    ('header', MSG_HEADER),
    ('position', c_double * 54),
    ('velocity', c_double * 54),
    ('torque', c_double * 54),
    ('temperature', c_double * 54),
]

MDF_MPL_RAW_PERCEPT = struct_anon_15 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 256

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 271
class struct_anon_16(Structure):
    pass

struct_anon_16.__slots__ = [
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
]
struct_anon_16._fields_ = [
    ('header', MSG_HEADER),
    ('ind_force', c_double * 3),
    ('mid_force', c_double * 3),
    ('rng_force', c_double * 3),
    ('lit_force', c_double * 3),
    ('thb_force', c_double * 3),
    ('ind_accel', c_double * 3),
    ('mid_accel', c_double * 3),
    ('rng_accel', c_double * 3),
    ('lit_accel', c_double * 3),
    ('thb_accel', c_double * 3),
]

MDF_MPL_SEGMENT_PERCEPTS = struct_anon_16 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 271

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 277
class struct_anon_17(Structure):
    pass

struct_anon_17.__slots__ = [
    'wrist_position',
    'joint_position',
]
struct_anon_17._fields_ = [
    ('wrist_position', c_double * 3),
    ('joint_position', c_double * 6),
]

MDF_ARMEO_FEEDBACK = struct_anon_17 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 277

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 283
class struct_anon_18(Structure):
    pass

struct_anon_18.__slots__ = [
    'header',
    'wrist_position',
    'joint_position',
]
struct_anon_18._fields_ = [
    ('header', MSG_HEADER),
    ('wrist_position', c_double * 3),
    ('joint_position', c_double * 6),
]

MDF_ARMEO_SERIAL_FEEDBACK = struct_anon_18 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 283

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 292
class struct_anon_19(Structure):
    pass

struct_anon_19.__slots__ = [
    'header',
    'position_mode',
    'reserved',
    'position_command',
    'joint_command',
    'j_angle_command',
]
struct_anon_19._fields_ = [
    ('header', MSG_HEADER),
    ('position_mode', c_int),
    ('reserved', c_int),
    ('position_command', c_double * 3),
    ('joint_command', c_double * 6),
    ('j_angle_command', c_double),
]

MDF_ARMEO_COMMAND = struct_anon_19 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 292

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 299
class struct_anon_20(Structure):
    pass

struct_anon_20.__slots__ = [
    'mode',
    'joint',
    'stiffness',
    'damping',
]
struct_anon_20._fields_ = [
    ('mode', c_int),
    ('joint', c_int),
    ('stiffness', c_double),
    ('damping', c_double),
]

MDF_ARMEO_CONFIG = struct_anon_20 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 299

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 306
class struct_anon_21(Structure):
    pass

struct_anon_21.__slots__ = [
    'min_edge',
    'max_edge',
    'wrist_range',
    'pro_sup_range',
]
struct_anon_21._fields_ = [
    ('min_edge', c_double * 3),
    ('max_edge', c_double * 3),
    ('wrist_range', c_double * 2),
    ('pro_sup_range', c_double * 2),
]

MDF_ARMEO_WKSPC = struct_anon_21 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 306

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 317
class struct_anon_22(Structure):
    pass

struct_anon_22.__slots__ = [
    'header',
    'endpts',
    't_hold',
    'velocity',
    'joint',
    'n_reps',
    'start',
    'reserved',
]
struct_anon_22._fields_ = [
    ('header', MSG_HEADER),
    ('endpts', c_double * 2),
    ('t_hold', c_double * 2),
    ('velocity', c_double),
    ('joint', c_int),
    ('n_reps', c_int),
    ('start', c_int),
    ('reserved', c_int),
]

MDF_ARMEO_JOINT_CONFIG = struct_anon_22 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 317

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 325
class struct_anon_23(Structure):
    pass

struct_anon_23.__slots__ = [
    'source_index',
    'reserved',
    'source_timestamp',
    'data',
]
struct_anon_23._fields_ = [
    ('source_index', c_int),
    ('reserved', c_int),
    ('source_timestamp', c_double),
    ('data', c_short * (10 * 128)),
]

MDF_RAW_CTSDATA = struct_anon_23 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 325

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 331
class struct_anon_24(Structure):
    pass

struct_anon_24.__slots__ = [
    'header',
    'source_timestamp',
    'data',
]
struct_anon_24._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double),
    ('data', c_short * (((2 * 10) * 2) * 128)),
]

MDF_SPM_CTSDATA = struct_anon_24 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 331

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 339
class struct_anon_25(Structure):
    pass

struct_anon_25.__slots__ = [
    'source_index',
    'reserved',
    'source_timestamp',
    'count_interval',
    'counts',
]
struct_anon_25._fields_ = [
    ('source_index', c_int),
    ('reserved', c_int),
    ('source_timestamp', c_double),
    ('count_interval', c_double),
    ('counts', c_ubyte * (128 * 5)),
]

MDF_RAW_SPIKECOUNT = struct_anon_25 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 339

SPIKE_COUNT_DATA_TYPE = c_ubyte # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 341

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 347
class struct_anon_26(Structure):
    pass

struct_anon_26.__slots__ = [
    'header',
    'source_timestamp',
    'count_interval',
    'counts',
]
struct_anon_26._fields_ = [
    ('header', MSG_HEADER),
    ('source_timestamp', c_double),
    ('count_interval', c_double),
    ('counts', SPIKE_COUNT_DATA_TYPE * (2 * (128 * 5))),
]

MDF_SPM_SPIKECOUNT = struct_anon_26 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 347

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 360
class struct_anon_27(Structure):
    pass

struct_anon_27.__slots__ = [
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
struct_anon_27._fields_ = [
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

SPIKE_SNIPPET = struct_anon_27 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 360

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 364
class struct_anon_28(Structure):
    pass

struct_anon_28.__slots__ = [
    'ss',
]
struct_anon_28._fields_ = [
    ('ss', SPIKE_SNIPPET * 25),
]

MDF_SPIKE_SNIPPET = struct_anon_28 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 364

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 379
class struct_anon_29(Structure):
    pass

struct_anon_29.__slots__ = [
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
struct_anon_29._fields_ = [
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

REJECTED_SNIPPET = struct_anon_29 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 379

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 383
class struct_anon_30(Structure):
    pass

struct_anon_30.__slots__ = [
    'rs',
]
struct_anon_30._fields_ = [
    ('rs', REJECTED_SNIPPET * 25),
]

MDF_REJECTED_SNIPPET = struct_anon_30 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 383

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 392
class struct_anon_31(Structure):
    pass

struct_anon_31.__slots__ = [
    'source_index',
    'channel',
    'source_timestamp',
    'data',
    'reserved',
]
struct_anon_31._fields_ = [
    ('source_index', c_int),
    ('channel', c_int),
    ('source_timestamp', c_double),
    ('data', c_uint),
    ('reserved', c_int),
]

MDF_DIGITAL_EVENT = struct_anon_31 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 392

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 398
class struct_anon_32(Structure):
    pass

struct_anon_32.__slots__ = [
    'header',
    'tag',
    'dof_vals',
]
struct_anon_32._fields_ = [
    ('header', MSG_HEADER),
    ('tag', c_char * 64),
    ('dof_vals', c_double * 30),
]

MDF_INPUT_DOF_DATA = struct_anon_32 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 398

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 409
class struct_anon_33(Structure):
    pass

struct_anon_33.__slots__ = [
    'header',
    'tag',
    'raw_vals',
    'calib_vals',
    'gesture',
    'glovetype',
    'hand',
    'reserved',
]
struct_anon_33._fields_ = [
    ('header', MSG_HEADER),
    ('tag', c_char * 64),
    ('raw_vals', c_double * 18),
    ('calib_vals', c_double * 18),
    ('gesture', c_int),
    ('glovetype', c_int),
    ('hand', c_int),
    ('reserved', c_int),
]

MDF_DATAGLOVE = struct_anon_33 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 409

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 437
class struct_anon_34(Structure):
    pass

struct_anon_34.__slots__ = [
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
struct_anon_34._fields_ = [
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

MDF_CERESTIM_CONFIG_MODULE = struct_anon_34 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 437

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 447
class struct_anon_35(Structure):
    pass

struct_anon_35.__slots__ = [
    'header',
    'stop',
    'numChans',
    'channel',
    'pattern',
    'reps',
    'reserved',
]
struct_anon_35._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('numChans', c_int),
    ('channel', c_int * 12),
    ('pattern', c_int * 12),
    ('reps', c_int),
    ('reserved', c_int),
]

MDF_CERESTIM_CONFIG_CHAN = struct_anon_35 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 447

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 457
class struct_anon_36(Structure):
    pass

struct_anon_36.__slots__ = [
    'header',
    'stop',
    'numChans',
    'channel',
    'pattern',
    'reps',
    'reserved',
]
struct_anon_36._fields_ = [
    ('header', MSG_HEADER),
    ('stop', c_int),
    ('numChans', c_int),
    ('channel', c_int * 64),
    ('pattern', c_int * 64),
    ('reps', c_int),
    ('reserved', c_int),
]

MDF_CERESTIM_CONFIG_CHAN_PRESAFETY = struct_anon_36 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 457

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 463
class struct_anon_37(Structure):
    pass

struct_anon_37.__slots__ = [
    'error',
    'config',
]
struct_anon_37._fields_ = [
    ('error', c_int),
    ('config', c_int),
]

MDF_CERESTIM_ERROR = struct_anon_37 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 463

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 479
class struct_anon_39(Structure):
    pass

struct_anon_39.__slots__ = [
    'handp',
    'handd',
    'head',
    'arms',
    'tag',
]
struct_anon_39._fields_ = [
    ('handp', c_char * 56),
    ('handd', c_char * 24),
    ('head', c_char * 16),
    ('arms', c_char * 24),
    ('tag', c_int),
]

MDF_RF_REPORT = struct_anon_39 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 479

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 485
class struct_anon_40(Structure):
    pass

struct_anon_40.__slots__ = [
    'record',
    'stop',
    'filename',
]
struct_anon_40._fields_ = [
    ('record', c_int),
    ('stop', c_int),
    ('filename', c_char * 256),
]

MDF_AJA_CONFIG = struct_anon_40 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 485

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 490
class struct_anon_41(Structure):
    pass

struct_anon_41.__slots__ = [
    'header',
    'timecode',
]
struct_anon_41._fields_ = [
    ('header', MSG_HEADER),
    ('timecode', c_char * 128),
]

MDF_AJA_TIMECODE = struct_anon_41 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 490

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 496
class struct_anon_42(Structure):
    pass

struct_anon_42.__slots__ = [
    'status',
    'reserved',
    'clipname',
]
struct_anon_42._fields_ = [
    ('status', c_int),
    ('reserved', c_int),
    ('clipname', c_char * 256),
]

MDF_AJA_STATUS = struct_anon_42 # C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 496

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __STDC__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __STDC_HOSTED__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GNUC__ = 4
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GNUC_MINOR__ = 8
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GNUC_PATCHLEVEL__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __VERSION__ = '4.8.1'
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_RELAXED = 0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_SEQ_CST = 5
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_ACQUIRE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_RELEASE = 3
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_ACQ_REL = 4
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_CONSUME = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FINITE_MATH_ONLY__ = 0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_INT__ = 4
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_LONG__ = 4
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_LONG_LONG__ = 8
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_SHORT__ = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_FLOAT__ = 4
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_DOUBLE__ = 8
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_LONG_DOUBLE__ = 12
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_SIZE_T__ = 4
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __CHAR_BIT__ = 8
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __BIGGEST_ALIGNMENT__ = 16
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ORDER_LITTLE_ENDIAN__ = 1234
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ORDER_BIG_ENDIAN__ = 4321
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ORDER_PDP_ENDIAN__ = 3412
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __BYTE_ORDER__ = __ORDER_LITTLE_ENDIAN__
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLOAT_WORD_ORDER__ = __ORDER_LITTLE_ENDIAN__
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_POINTER__ = 4
except:
    pass

__SIZE_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__PTRDIFF_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__WCHAR_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__WINT_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INTMAX_TYPE__ = c_longlong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINTMAX_TYPE__ = c_ulonglong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__CHAR16_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__CHAR32_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__SIG_ATOMIC_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT8_TYPE__ = c_char # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT16_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT32_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT64_TYPE__ = c_longlong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT8_TYPE__ = c_ubyte # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT16_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT32_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT64_TYPE__ = c_ulonglong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_LEAST8_TYPE__ = c_char # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_LEAST16_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_LEAST32_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_LEAST64_TYPE__ = c_longlong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_LEAST8_TYPE__ = c_ubyte # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_LEAST16_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_LEAST32_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_LEAST64_TYPE__ = c_ulonglong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_FAST8_TYPE__ = c_char # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_FAST16_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_FAST32_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INT_FAST64_TYPE__ = c_longlong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_FAST8_TYPE__ = c_ubyte # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_FAST16_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_FAST32_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINT_FAST64_TYPE__ = c_ulonglong # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__INTPTR_TYPE__ = c_int # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

__UINTPTR_TYPE__ = c_uint # c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GXX_ABI_VERSION = 1002
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SCHAR_MAX__ = 127
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SHRT_MAX__ = 32767
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_MAX__ = 2147483647
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LONG_MAX__ = 2147483647L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LONG_LONG_MAX__ = 9223372036854775807L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WCHAR_MAX__ = 65535
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WCHAR_MIN__ = 0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WINT_MAX__ = 65535
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WINT_MIN__ = 0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __PTRDIFF_MAX__ = 2147483647
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZE_MAX__ = 4294967295L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INTMAX_MAX__ = 9223372036854775807L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINTMAX_MAX__ = 18446744073709551615L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIG_ATOMIC_MAX__ = 2147483647
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIG_ATOMIC_MIN__ = ((-__SIG_ATOMIC_MAX__) - 1)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT8_MAX__ = 127
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT16_MAX__ = 32767
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT32_MAX__ = 2147483647
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT64_MAX__ = 9223372036854775807L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT8_MAX__ = 255
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT16_MAX__ = 65535
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT32_MAX__ = 4294967295L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT64_MAX__ = 18446744073709551615L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_LEAST8_MAX__ = 127
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
def __INT8_C(c):
    return c

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_LEAST16_MAX__ = 32767
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
def __INT16_C(c):
    return c

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_LEAST32_MAX__ = 2147483647
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
def __INT32_C(c):
    return c

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_LEAST64_MAX__ = 9223372036854775807L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_LEAST8_MAX__ = 255
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
def __UINT8_C(c):
    return c

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_LEAST16_MAX__ = 65535
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
def __UINT16_C(c):
    return c

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_LEAST32_MAX__ = 4294967295L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_LEAST64_MAX__ = 18446744073709551615L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_FAST8_MAX__ = 127
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_FAST16_MAX__ = 32767
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_FAST32_MAX__ = 2147483647
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INT_FAST64_MAX__ = 9223372036854775807L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_FAST8_MAX__ = 255
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_FAST16_MAX__ = 65535
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_FAST32_MAX__ = 4294967295L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINT_FAST64_MAX__ = 18446744073709551615L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __INTPTR_MAX__ = 2147483647
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __UINTPTR_MAX__ = 4294967295L
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_EVAL_METHOD__ = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC_EVAL_METHOD__ = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_RADIX__ = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_MANT_DIG__ = 24
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_DIG__ = 6
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_MIN_EXP__ = (-125)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_MIN_10_EXP__ = (-37)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_MAX_EXP__ = 128
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_MAX_10_EXP__ = 38
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_DECIMAL_DIG__ = 9
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_MAX__ = 3.4028234663852886e+38
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_MIN__ = 1.1754943508222875e-38
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_EPSILON__ = 1.1920928955078125e-07
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_DENORM_MIN__ = 1.401298464324817e-45
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_HAS_DENORM__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_HAS_INFINITY__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __FLT_HAS_QUIET_NAN__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_MANT_DIG__ = 53
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_DIG__ = 15
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_MIN_EXP__ = (-1021)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_MIN_10_EXP__ = (-307)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_MAX_EXP__ = 1024
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_MAX_10_EXP__ = 308
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_DECIMAL_DIG__ = 17
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_MAX__ = 1.7976931348623157e+308
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_MIN__ = 2.2250738585072014e-308
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_EPSILON__ = 2.220446049250313e-16
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_DENORM_MIN__ = 5e-324
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_HAS_DENORM__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_HAS_INFINITY__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DBL_HAS_QUIET_NAN__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_MANT_DIG__ = 64
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_DIG__ = 18
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_MIN_EXP__ = (-16381)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_MIN_10_EXP__ = (-4931)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_MAX_EXP__ = 16384
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_MAX_10_EXP__ = 4932
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DECIMAL_DIG__ = 21
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_MAX__ = float('inf')
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_MIN__ = 0.0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_EPSILON__ = 1.0842021724855044e-19
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_DENORM_MIN__ = 0.0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_HAS_DENORM__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_HAS_INFINITY__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __LDBL_HAS_QUIET_NAN__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC32_MANT_DIG__ = 7
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC32_MIN_EXP__ = (-94)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC32_MAX_EXP__ = 97
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC64_MANT_DIG__ = 16
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC64_MIN_EXP__ = (-382)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC64_MAX_EXP__ = 385
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC128_MANT_DIG__ = 34
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC128_MIN_EXP__ = (-6142)
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DEC128_MAX_EXP__ = 6145
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GNUC_GNU_INLINE__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __NO_INLINE__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_HAVE_SYNC_COMPARE_AND_SWAP_1 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_HAVE_SYNC_COMPARE_AND_SWAP_2 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_HAVE_SYNC_COMPARE_AND_SWAP_4 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_HAVE_SYNC_COMPARE_AND_SWAP_8 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_BOOL_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_CHAR_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_CHAR16_T_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_CHAR32_T_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_WCHAR_T_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_SHORT_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_INT_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_LONG_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_LLONG_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_TEST_AND_SET_TRUEVAL = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_ATOMIC_POINTER_LOCK_FREE = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GCC_HAVE_DWARF2_CFI_ASM = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __PRAGMA_REDEFINE_EXTNAME = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_WCHAR_T__ = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_WINT_T__ = 2
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __SIZEOF_PTRDIFF_T__ = 4
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __i386 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __i386__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    i386 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_HLE_ACQUIRE = 65536
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __ATOMIC_HLE_RELEASE = 131072
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __i686 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __i686__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __pentiumpro = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __pentiumpro__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __code_model_32__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    _X86_ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GXX_MERGED_TYPEINFO_NAMES = 0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __GXX_TYPEINFO_EQUALITY_INLINE = 0
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __MSVCRT__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __MINGW32__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    _WIN32 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WIN32 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WIN32__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    WIN32 = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WINNT = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __WINNT__ = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    WINNT = 1
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    _INTEGRAL_MAX_BITS = 64
except:
    pass

# c:\\users\\hrnel\\appdata\\local\\temp\\tmpksezmu.h: 1
try:
    __DECIMAL_BID_FORMAT__ = 1
except:
    pass

__const = c_int # <command-line>: 5

# <command-line>: 8
try:
    CTYPESGEN = 1
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 5
try:
    DEFAULT_MM_IP = 'localhost:7111'
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 8
try:
    MAX_SPIKE_SOURCES = 2
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 9
try:
    MAX_SPIKE_CHANS_PER_SOURCE = 128
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 10
try:
    MAX_UNITS_PER_CHAN = 5
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 11
try:
    MAX_TOTAL_SPIKE_CHANS_PER_SOURCE = (MAX_SPIKE_CHANS_PER_SOURCE * MAX_UNITS_PER_CHAN)
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 12
try:
    MAX_TOTAL_SPIKE_CHANS = (MAX_SPIKE_SOURCES * MAX_TOTAL_SPIKE_CHANS_PER_SOURCE)
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 13
try:
    LFPSAMPLES_PER_HEARTBEAT = 10
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 14
try:
    RAW_COUNTS_PER_SAMPLE = 2
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 15
try:
    SNIPPETS_PER_MESSAGE = 25
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 16
try:
    SAMPLES_PER_SNIPPET = 48
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 17
try:
    MAX_DATAGLOVE_SENSORS = 18
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 18
try:
    NUM_DOMAINS = 6
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 19
try:
    MAX_COMMAND_DIMS = 30
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 20
try:
    MPL_RAW_PERCEPT_DIMS = 54
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 22
try:
    NUM_STIM_CHANS = 64
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 23
try:
    MAX_STIM_CHANS_ON = 12
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 24
try:
    MAX_GROBOT_JOINTS = 28
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 25
try:
    MAX_CS_CONFIGS = 16
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 27
try:
    GRIP_DIMS_R = 1
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 28
try:
    GRIP_DIMS_L = 1
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 31
try:
    NoResult = (-1)
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 32
try:
    SuccessfulTrial = 1
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 33
try:
    BadTrial = 2
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 34
try:
    ManualProceed = 4
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 35
try:
    ManualFail = 8
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 41
try:
    MID_JSTICK_COMMAND = 10
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 42
try:
    MID_COMBINER = 11
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 43
try:
    MID_CEREBUS = 12
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 44
try:
    MID_INPUT_TRANSFORM = 20
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 45
try:
    MID_EXTRACTION = 30
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 46
try:
    MID_LFPEXTRACTION = 31
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 47
try:
    MID_MPL_CONTROL = 40
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 48
try:
    MID_ACTIVE_ASSIST = 50
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 49
try:
    MID_MPL_FEEDBACK = 60
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 50
try:
    MID_EXECUTIVE = 70
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 51
try:
    MID_StimVoltageMonitor = 77
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 52
try:
    MID_GENERIC = 80
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 53
try:
    MID_MESSAGERATES = 81
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 54
try:
    MID_VISUALIZATION = 82
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 55
try:
    MID_VIDEO_LOGGER = 83
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 56
try:
    MID_AUDIO_LOGGER = 84
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 57
try:
    MID_DATAGLOVE_CONTROL = 85
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 58
try:
    MID_BIASMODULE = 86
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 59
try:
    MID_CURSOR = 87
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 60
try:
    MID_SOUNDPLAYER = 90
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 61
try:
    MID_RFIELD = 91
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 62
try:
    MID_RFACTIVITY = 92
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 63
try:
    MID_PICS = 93
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 64
try:
    MID_CREATEBUFFER = 35
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 65
try:
    MID_AJA_CONTROL = 65
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 67
try:
    MID_HOCOMA_FEEDBACK = 61
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 68
try:
    MID_ARMEO_CONTROLLER = 42
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 69
try:
    MID_ARMEO_RTMA = 43
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 71
try:
    MID_STIM_SAFETY_MODULE = 95
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 72
try:
    MID_SENSOR_STIM_TRANS_MODULE = 96
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 73
try:
    MID_CERESTIM_CONTROL = 97
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 76
try:
    MT_FINISHED_COMMAND = 1700
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 77
try:
    MT_CONTROL_SPACE_COMMAND = 1702
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 78
try:
    MT_CONTROL_SPACE_POS_COMMAND = 1710
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 79
try:
    MT_CONTROL_SPACE_FEEDBACK = 1701
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 80
try:
    MT_MPL_RAW_PERCEPT = 1703
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 81
try:
    MT_MPL_SEGMENT_PERCEPTS = 1711
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 82
try:
    MT_ARMEO_FEEDBACK = 1704
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 83
try:
    MT_ARMEO_COMMAND = 1705
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 84
try:
    MT_ARMEO_CONFIG = 1706
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 85
try:
    MT_ARMEO_WKSPC = 1707
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 86
try:
    MT_ARMEO_SERIAL_FEEDBACK = 1708
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 87
try:
    MT_ARMEO_JOINT_CONFIG = 1709
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 89
try:
    MT_RAW_SPIKECOUNT = 1800
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 90
try:
    MT_SPM_SPIKECOUNT = 1801
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 91
try:
    MT_SPIKE_SNIPPET = 1802
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 93
try:
    MT_RAW_CTSDATA = 1803
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 94
try:
    MT_SPM_CTSDATA = 1804
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 95
try:
    MT_REJECTED_SNIPPET = 1805
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 96
try:
    MT_DIGITAL_EVENT = 1806
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 98
try:
    MT_INPUT_DOF_DATA = 1850
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 100
try:
    MT_DATAGLOVE = 1860
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 102
try:
    MT_TASK_STATE_CONFIG = 1900
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 103
try:
    MT_PHASE_RESULT = 1901
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 104
try:
    MT_EXTRACTION_RESPONSE = 1902
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 106
try:
    MT_EM_ADAPT_NOW = 2000
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 107
try:
    MT_EM_CONFIGURATION = 2001
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 108
try:
    MT_TDMS_CREATE = 2002
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 109
try:
    MT_RF_REPORT = 2003
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 110
try:
    MT_PICDISPLAY = 2004
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 112
try:
    MT_STIMDATA = 2005
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 114
try:
    MT_HSTLOG = 3000
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 115
try:
    MT_TFD = 3001
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 117
try:
    MT_PLAYSOUND = 3100
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 119
try:
    MT_AJA_CONFIG = 3200
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 120
try:
    MT_AJA_TIMECODE = 3201
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 121
try:
    MT_AJA_STATUS = 3202
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 122
try:
    MT_AJA_STATUS_REQUEST = 3203
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 125
try:
    MT_CERESTIM_CONFIG_MODULE = 4000
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 126
try:
    MT_CERESTIM_CONFIG_CHAN_PRESAFETY = 4001
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 127
try:
    MT_CERESTIM_CONFIG_CHAN = 4002
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 128
try:
    MT_CERESTIM_ERROR = 4003
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 129
try:
    MT_CERESTIM_ALIVE = 4004
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 130
try:
    MT_CS_TRAIN_END = 4005
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 133
try:
    TAG_LENGTH = 64
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 138
try:
    MPL_AT_ARM_EPV_FING_JV = 0
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 139
try:
    MPL_AT_ARM_EPV_FING_JP = 1
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 140
try:
    MPL_AT_ARM_JV_FING_JP = 2
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 141
try:
    MPL_AT_ALL_JV = 3
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 142
try:
    MPL_AT_ALL_JP = 4
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 143
try:
    MPL_AT_ARM_EPP_FING_JP = 5
except:
    pass

# C:\\hst2\\src\\Common\\include\\rp3_hst_config.h: 146
try:
    TFD_FREQ_BINS = 20
except:
    pass

# No inserted files


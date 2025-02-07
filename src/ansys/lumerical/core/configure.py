import os
import platform
import inspect
from ctypes import CDLL, Structure, Union, c_void_p, c_char_p, POINTER, c_ulonglong, c_double, c_char, c_uint, c_int
from contextlib import contextmanager
import re

def remoteModuleOn(remoteArgs):
    return type(remoteArgs) is dict and len(remoteArgs) > 0

class InteropPaths:
    """
    A class used to manage the paths and environment variables for Lumerical's interop library.
    Attributes
    ----------
    INTEROPLIBDIR : str
        Directory path where the interop library is located.
    INTEROPLIB_FILENAME : str
        Filename of the interop library.
    INTEROPLIB : str
        Full path to the interop library.
    ENVIRONPATH : str
        Environment path variable including the path to the interop library.
    Methods
    -------
    setLumericalInstallPath(lumerical_path)
        Sets the installation path for Lumerical software.
    autoInitInstallPath()
        Automatically initializes the installation path based on the operating system.
    initLibraryEnv(remoteArgs)
        Initializes the library environment based on whether remote arguments are provided.
    """
    LUMERICALINSTALLDIR = ""
    INTEROPLIBDIR = ""
    INTEROPLIB_FILENAME = ""
    INTEROPLIB = ""
    ENVIRONPATH = ""

    @classmethod
    def setLumericalInstallPath(cls, lumerical_path):
        cls.LUMERICALINSTALLDIR = lumerical_path
        cls.INTEROPLIBDIR = os.path.join(lumerical_path, "api/python/")

    @classmethod
    def autoInitInstallPath(cls):
        """
        Automatically initializes the Lumerical installation path based on the operating system.
        This method attempts to guess the base installation directory for Lumerical software
        based on the operating system. It then searches for the latest version of the software
        within that directory and sets the class attributes `LUMERICALINSTALLDIR` and `INTEROPLIBDIR`
        accordingly. If the installation directory cannot be found, a warning message is printed.
        Returns:
            None
        """
        if platform.system() == 'Windows':
            guess_base = "C:\\Program Files\\Lumerical\\"
        elif platform.system() == 'Linux':
            guess_base = "/opt/lumerical/"
        elif platform.system() == 'Darwin':
            guess_base = "/Applications/Lumerical/"
        else:
            print("Warning: Unable to find Lumerical installation directory. Please run setLumericalInstallPath before starting a session.")
            return

        if os.path.exists(guess_base):
            found_install = False
            latest_ver_year = 25
            latest_ver_release = 1
            for dir in os.listdir(guess_base):
                if os.path.isdir(os.path.join(guess_base, dir)):
                    match = re.match(r'v(\d{2})(\d)', dir)
                    if match:
                        found_install = True
                        ver_year = int(match.group(1))
                        ver_maj = int(match.group(2))
                        if ver_year > latest_ver_year or (ver_year == latest_ver_year and ver_maj > latest_ver_release):
                            latest_ver_year = ver_year
                            latest_ver_release = ver_maj

            if found_install:
                cls.LUMERICALINSTALLDIR = os.path.join(guess_base, dir)
                cls.INTEROPLIBDIR = os.path.join(guess_base, dir, "api/python/")
            else:
                print("Warning: Unable to find Lumerical installation directory. Please run setLumericalInstallPath before starting a session.")

    @classmethod
    def initLibraryEnv(cls, remoteArgs):
        if remoteModuleOn(remoteArgs):
            if platform.system() == 'Windows':
                cls.INTEROPLIB_FILENAME = "interopapi-remote.dll"
            if platform.system() == 'Linux':
                cls.INTEROPLIB_FILENAME = "libinteropapi-remote.so.1"
        else:
            if platform.system() == 'Windows':
                cls.INTEROPLIB_FILENAME = "interopapi.dll"
            if platform.system() == 'Linux':
                cls.INTEROPLIB_FILENAME = "libinterop-api.so.1"

        if len(cls.INTEROPLIB_FILENAME) == 0 or len(cls.INTEROPLIBDIR) == 0:
            raise ImportError("Library name or directory were not defined.")

        if platform.system() == 'Windows' or platform.system() == 'Linux':
            MODERN_LUMLDIR = os.path.join(cls.LUMERICALINSTALLDIR, "/bin")
            cls.INTEROPLIB = os.path.join(cls.INTEROPLIBDIR, cls.INTEROPLIB_FILENAME)
            if platform.system() == 'Windows':
                cls.ENVIRONPATH = MODERN_LUMLDIR + ";" + os.environ['PATH']
            elif platform.system() == 'Linux':
                cls.ENVIRONPATH = MODERN_LUMLDIR + ":" + os.environ['PATH']
        elif platform.system() == 'Darwin':
            cls.INTEROPLIB = cls.INTEROPLIBDIR + "/libinterop-api.1.dylib"
            FDTD_SUFFIX = "/FDTD Solutions.app/Contents/MacOS"
            MODE_SUFFIX = "/MODE Solutions.app/Contents/MacOS"
            DEVC_SUFFIX = "/DEVICE.app/Contents/MacOS"
            INTC_SUFFIX = "/INTERCONNECT.app/Contents/MacOS"
            MODERN_FDTDDIR = cls.LUMERICALINSTALLDIR + "/Contents/Applications" + FDTD_SUFFIX
            MODERN_MODEDIR = cls.LUMERICALINSTALLDIR + "/Contents/Applications" + MODE_SUFFIX
            MODERN_DEVCDIR = cls.LUMERICALINSTALLDIR + "/Contents/Applications" + DEVC_SUFFIX
            MODERN_INTCDIR = cls.LUMERICALINSTALLDIR + "/Contents/Applications" + INTC_SUFFIX
            cls.ENVIRONPATH = MODERN_FDTDDIR + ":" + MODERN_MODEDIR + ":" + MODERN_DEVCDIR + ":" + MODERN_INTCDIR + ":" + os.environ['PATH']

class Session(Structure):
    _fields_ = [("p", c_void_p)]

class LumString(Structure):
    _fields_ = [("len", c_ulonglong), ("str", POINTER(c_char))]

class LumMat(Structure):
    _fields_ = [("mode", c_uint),
                ("dim", c_ulonglong),
                ("dimlst", POINTER(c_ulonglong)),
                ("data", POINTER(c_double))]

## For incomplete types where the type is not defined before it's used.
## An example is the LumStruct that contains a member of type Any but the type Any is still undefined
## Review https://docs.python.org/2/library/ctypes.html#incomplete-types for more information.
class LumNameValuePair(Structure):
    pass


class LumStruct(Structure):
    pass


class LumList(Structure):
    pass


class ValUnion(Union):
    pass

class Any(Structure):
    pass

LumNameValuePair._fields_ = [("name", LumString), ("value", POINTER(Any))]
LumStruct._fields_ = [("size", c_ulonglong), ("elements", POINTER(POINTER(Any)))]
LumList._fields_ = [("size", c_ulonglong), ("elements", POINTER(POINTER(Any)))]
ValUnion._fields_ = [("doubleVal", c_double),
                     ("strVal", LumString),
                     ("matrixVal", LumMat),
                     ("structVal", LumStruct),
                     ("nameValuePairVal", LumNameValuePair),
                     ("listVal", LumList)]
Any._fields_ = [("type", c_int), ("val", ValUnion)]


@contextmanager
def environ(env):
    """Temporarily set environment variables inside the context manager and
    fully restore previous environment afterwards
    """
    original_env = {key: os.getenv(key) for key in env}
    os.environ.update(env)
    try:
        yield
    finally:
        for key, value in original_env.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value

def initLib(remoteArgs):
    InteropPaths.initLibraryEnv(remoteArgs)

    if not os.path.isfile(InteropPaths.INTEROPLIB):
        raise ImportError("Unable to find file " + InteropPaths.INTEROPLIB)

    with environ({"PATH": InteropPaths.ENVIRONPATH}):
        iapi = CDLL(InteropPaths.INTEROPLIB)
        # print('\033[93m' + "Library loaded: " + INTEROPLIB + '\033[0m')

        iapi.appOpen.restype = Session
        iapi.appOpen.argtypes = [c_char_p, POINTER(c_ulonglong)]

        iapi.appClose.restype = None
        iapi.appClose.argtypes = [Session]

        iapi.appEvalScript.restype = int
        iapi.appEvalScript.argtypes = [Session, c_char_p]

        iapi.appGetVar.restype = int
        iapi.appGetVar.argtypes = [Session, c_char_p, POINTER(POINTER(Any))]

        iapi.appPutVar.restype = int
        iapi.appPutVar.argtypes = [Session, c_char_p, POINTER(Any)]

        iapi.allocateLumDouble.restype = POINTER(Any)
        iapi.allocateLumDouble.argtypes = [c_double]

        iapi.allocateLumString.restype = POINTER(Any)
        iapi.allocateLumString.argtypes = [c_ulonglong, c_char_p]

        iapi.allocateLumMatrix.restype = POINTER(Any)
        iapi.allocateLumMatrix.argtypes = [c_ulonglong, POINTER(c_ulonglong)]

        iapi.allocateComplexLumMatrix.restype = POINTER(Any)
        iapi.allocateComplexLumMatrix.argtypes = [c_ulonglong, POINTER(c_ulonglong)]

        iapi.allocateLumNameValuePair.restype = POINTER(Any)
        iapi.allocateLumNameValuePair.argtypes = [c_ulonglong, c_char_p, POINTER(Any)]

        iapi.allocateLumStruct.restype = POINTER(Any)
        iapi.allocateLumStruct.argtypes = [c_ulonglong, POINTER(POINTER(Any))]

        iapi.allocateLumList.restype = POINTER(Any)
        iapi.allocateLumList.argtypes = [c_ulonglong, POINTER(POINTER(Any))]

        iapi.freeAny.restype = None
        iapi.freeAny.argtypes = [POINTER(Any)]

        iapi.appGetLastError.restype = POINTER(LumString)
        iapi.appGetLastError.argtypes = None

        return iapi

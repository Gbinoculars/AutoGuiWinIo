import platform
import ctypes
from ctypes import wintypes


class tagPhysStruct(ctypes.Structure):
    _fields_ = [	("dwPhysMemSizeInBytes", wintypes.DWORD),
	                ("pvPhysAddress",wintypes.DWORD),
	                ("PhysicalMemoryHandle",wintypes.DWORD),
	                ("pvPhysMemLin" , wintypes.DWORD),
	                ("pvPhysSection",wintypes.DWORD)
                ]


class F_WinIo:
    # bool _stdcall InitializeWinIo()
    InitializeWinIo = ctypes.WINFUNCTYPE(wintypes.BOOL)
    P_InitializeWinIo = None
    # WINIO_API void _stdcall ShutdownWinIo();
    ShutdownWinIo = ctypes.WINFUNCTYPE(ctypes.c_void_p)
    P_ShutdownWinIo = None
    # WINIO_API PBYTE _stdcall MapPhysToLin(tagPhysStruct &PhysStruct);
    MapPhysToLin = ctypes.WINFUNCTYPE(wintypes.PBYTE,tagPhysStruct)
    P_MapPhysToLin = None
    # WINIO_API bool _stdcall UnmapPhysicalMemory(tagPhysStruct &PhysStruct);
    UnmapPhysicalMemory = ctypes.WINFUNCTYPE(wintypes.BOOL,tagPhysStruct)
    P_UnmapPhysicalMemory = None
    # WINIO_API bool _stdcall GetPhysLong(PBYTE pbPhysAddr, PDWORD pdwPhysVal);
    GetPhysLong = ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.PBYTE,wintypes.PDWORD)
    P_GetPhysLong = None
    # WINIO_API bool _stdcall SetPhysLong(PBYTE pbPhysAddr, DWORD dwPhysVal);
    SetPhysLong = ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.PBYTE,wintypes.PDWORD)
    P_SetPhysLong = None
    # WINIO_API bool _stdcall GetPortVal(WORD wPortAddr, PDWORD pdwPortVal, BYTE bSize);
    GetPortVal = ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.WORD,wintypes.PDWORD,wintypes.BYTE)
    P_GetPortVal = None
    # WINIO_API bool _stdcall SetPortVal(WORD wPortAddr, DWORD dwPortVal, BYTE bSize);
    SetPortVal = ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.WORD,wintypes.DWORD,wintypes.BYTE)
    P_SetPortVal = None
    # WINIO_API bool _stdcall InstallWinIoDriver(PWSTR pszWinIoDriverPath, bool IsDemandLoaded = false);
    InstallWinIoDriver = ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.PWCHAR,wintypes.BOOL)
    P_InstallWinIoDriver = None
    # WINIO_API bool _stdcall RemoveWinIoDriver();
    RemoveWinIoDriver = ctypes.WINFUNCTYPE(wintypes.BOOL)
    P_RemoveWinIoDriver = None


def InitWinIo(dllsRootPath):
    if platform.system() != "Windows":
        print("Only Support Windows OS")
        return -1
    
    import os

    if platform.architecture()[0] == '64bit':
        LIB_NAME = os.path.join(dllsRootPath, "WinIo64.dll")
    if platform.architecture()[0] == '32bit':
        LIB_NAME = os.path.join(dllsRootPath, "WinIo32.dll")

    kernel32Dll = ctypes.windll.kernel32
    
    F_LoadLibrary = kernel32Dll.LoadLibraryA
    F_LoadLibrary.restype = wintypes.HMODULE
    F_LoadLibrary.argtypes = [ctypes.c_char_p]

    HMODULE_WinIo = F_LoadLibrary(ctypes.c_char_p(LIB_NAME.encode("ascii")))
    if not HMODULE_WinIo:
        return -1
    
    F_GetProcAddress = kernel32Dll.GetProcAddress
    F_GetProcAddress.restype = ctypes.c_void_p
    F_GetProcAddress.argtypes = [wintypes.HMODULE, ctypes.c_char_p]
    F_WinIo.P_InitializeWinIo = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("InitializeWinIo".encode("ascii")))
    
    if not F_WinIo.InitializeWinIo:
        print("Cannot find function: InitializeWinIo with error: " + str(ctypes.GetLastError()))
        return -1
    
    isWinIoInitialized = F_WinIo.InitializeWinIo(F_WinIo.P_InitializeWinIo)()
    if not isWinIoInitialized:
        print("Fail InitializeWinIo with error: " + str(ctypes.GetLastError()))
        return -1
    
    F_WinIo.P_ShutdownWinIo = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("ShutdownWinIo".encode("ascii")))
    if not F_WinIo.P_ShutdownWinIo:
        print("Cannot find function: ShutdownWinIo with error: " + str(ctypes.GetLastError()))
        return -1
    
    F_WinIo.P_GetPortVal = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("GetPortVal".encode("ascii")))
    F_WinIo.P_SetPortVal = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("SetPortVal".encode("ascii")))
    F_WinIo.P_MapPhysToLin = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("MapPhysToLin".encode("ascii")))
    F_WinIo.P_UnmapPhysicalMemory = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("UnmapPhysicalMemory".encode("ascii")))
    F_WinIo.P_GetPhysLong = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("GetPhysLong".encode("ascii")))
    F_WinIo.P_RemoveWinIoDriver = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("RemoveWinIoDriver".encode("ascii")))
    F_WinIo.P_SetPhysLong = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("SetPhysLong".encode("ascii")))
    F_WinIo.P_InstallWinIoDriver = F_GetProcAddress(HMODULE_WinIo,ctypes.c_char_p("InstallWinIoDriver".encode("ascii")))
    
    return 0


def ShutDownWinIo():
    F_WinIo.ShutdownWinIo(F_WinIo.P_ShutdownWinIo)()
    return 0
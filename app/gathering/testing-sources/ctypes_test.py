import ctypes
import os


def ram():
    kernel32 = ctypes.windll.kernel32
    c_ulong = ctypes.c_ulong

    class MEMORYSTATUS(ctypes.Structure):
        _fields_ = [
            ('dwLength', c_ulong),
            ('dwMemoryLoad', c_ulong),
            ('dwTotalPhys', c_ulong),
            ('dwAvailPhys', c_ulong),
            ('dwTotalPageFile', c_ulong),
            ('dwAvailPageFile', c_ulong),
            ('dwTotalVirtual', c_ulong),
            ('dwAvailVirtual', c_ulong)
        ]

    memoryStatus = MEMORYSTATUS()
    memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
    kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
    mem = memoryStatus.dwTotalPhys / (1024 * 1024)
    availRam = memoryStatus.dwAvailPhys / (1024 * 1024)
    if mem >= 1000:
        mem = mem / 1000
        totalRam = str(mem) + ' GB'
    else:
        #        mem = mem/1000000
        totalRam = str(mem) + ' MB'
    return (totalRam, availRam)


def _disk_c():
    drive = str(os.getenv("SystemDrive"))
    freeuser = ctypes.c_int64()
    total = ctypes.c_int64()
    free = ctypes.c_int64()
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive,
                                               ctypes.byref(freeuser),
                                               ctypes.byref(total),
                                               ctypes.byref(free))
    return freeuser.value


print(_disk_c())
print(ram())

from ctypes import *


D3DKMT_HANDLE = c_ulong

class D3DKMT_QUERYRESOURCEINFO(Structure):
    _fields_ = [
        ("hDevice", D3DKMT_HANDLE),
        ("hDevice", D3DKMT_HANDLE),
        ("pPrivateRuntimeData", c_void_p),
        ("PrivateRuntimeDataSize", c_uint),
        ("TotalPrivateDriverDataSize", c_uint),
        ("ResourcePrivateDriverDataSize", c_uint),
        ("NumAllocations", c_uint),
    ]


class LUID(Structure):
    _fields_ = [
        ("LowPart", c_uint),
        ("HighPart", c_long)
    ]

class D3DKMT_ADAPTERINFO(Structure):
    _fields_ = [
        ("hAdapter", D3DKMT_HANDLE),
        ("AdapterLuid", LUID),
        ("NumOfSources", c_ulong),
        ("BbPresentMoveRegionsPreferred", c_bool)
    ]


class D3DKMT_ENUMADAPTERS(Structure):
    _fields_ = [
        ("NumAdapters", c_ulong),
        ("Adapters", D3DKMT_ADAPTERINFO * 16)
    ]

adapter_array = D3DKMT_ENUMADAPTERS()

adapter_array.NumAdapters = 2

windll.gdi32.D3DKMTEnumAdapters(pointer(adapter_array))

print(adapter_array)
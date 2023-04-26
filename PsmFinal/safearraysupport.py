# very thin safearray support
from ctypes import *
from comtypes.typeinfo import SAFEARRAYBOUND
from comtypes.automation import VARIANT, VARTYPE
from comtypes.automation import VT_VARIANT, VT_R4, VT_R8, VT_I1, VT_I2, VT_I4, VT_INT, VT_UI1, VT_UI2, VT_UI4, VT_UINT

class SAFEARRAY(Structure):
    _fields_ = [("cDims", c_ushort),
                ("fFeatures", c_ushort),
                ("cbElements", c_ulong),
                ("cLocks", c_ulong),
                ("pvData", c_void_p),
                ("rgsabound", SAFEARRAYBOUND * 1)]

    def dump(self):
        print ("cDims", self.cDims)
        print ("fFeatures 0x%x" % self.fFeatures)
        print ("cLocks", self.cLocks)
        print ("cbElements", self.cbElements)


    def __getitem__(self, index):
        ix = c_int(index)
        data = c_double()
        res = windll.oleaut32.SafeArrayGetElement(byref(self), byref(ix), byref(data))
        if res:
            raise WinError(res)
        return data.value

    def __iter__(self):
        ix = c_int()
        data = c_double()
        get = windll.oleaut32.SafeArrayGetElement
        while 1:
            if get(byref(self), byref(ix), byref(data)):
                raise StopIteration
            yield data.value
            ix.value += 1

windll.oleaut32.SafeArrayCreateVectorEx.restype = POINTER(SAFEARRAY)

def SafeArray_FromSequence(seq):
    """Create a one dimensional safearray of type VT_VARIANT from a
    sequence of Python objects
    """
    psa = windll.oleaut32.SafeArrayCreateVectorEx(VT_VARIANT, 0, len(seq), None)
    for index, elem in enumerate(seq):
        oledll.oleaut32.SafeArrayPutElement(psa, byref(c_long(index)), byref(VARIANT(elem)))
    return psa

def SafeArray_FromArray(arr):
    """Create a one dimensional safearray of a numeric type from an
    array instance"""
    TYPECODE = {
        "d": VT_R8,
        "f": VT_R4,
        "l": VT_I4,
        "i": VT_INT,
        "h": VT_I2,
        "b": VT_I1,
        "I": VT_UINT,
        "L": VT_UI4,
        "H": VT_UI2,
        "B": VT_UI1,
        }

    vt = TYPECODE[arr.typecode]
    psa = windll.oleaut32.SafeArrayCreateVectorEx(vt, 0, len(arr), None)
    ptr = c_void_p()
    oledll.oleaut32.SafeArrayAccessData(psa, byref(ptr))
    memmove(ptr, arr.buffer_info()[0], len(arr) * arr.itemsize)
    oledll.oleaut32.SafeArrayUnaccessData(psa)
    return vt, psa

################################################################

def _get_row(ctype, psa, dim, indices, upperbounds):
    # loop over the index of dimension 'dim'
    # we have to restore the index of the dimension we're looping over
    restore = indices[dim]

    result = []
    for i in range(indices[dim], upperbounds[dim]+1):
        indices[dim] = i
        if dim+1 == len(indices):
            oledll.oleaut32.SafeArrayGetElement(psa, indices, byref(ctype))
            result.append(ctype.value)
        else:
            result.append(_get_row(ctype, psa, dim+1, indices, upperbounds))
    indices[dim] = restore
    return tuple(result) # for compatibility with pywin32.

def _get_ubound(psa, dim):
    # Return the upper bound of a dimension in a safearray
    ubound = c_long()
    oledll.oleaut32.SafeArrayGetUBound(psa, dim+1, byref(ubound))
    return ubound.value

def _get_lbound(psa, dim):
    # Return the lower bound of a dimension in a safearray
    lb = c_long()
    oledll.oleaut32.SafeArrayGetLBound(psa, dim+1, byref(lb))
    return lb.value

_VT2CTYPE = {
    VT_R8: c_double,
    VT_R4: c_float,
    VT_I4: c_long,
    VT_INT: c_int,
    VT_I2: c_short,
    VT_I1: c_byte,
    VT_UI4: c_ulong,
    VT_UINT: c_uint,
    VT_UI2: c_ushort,
    VT_UI1: c_ubyte,
    VT_VARIANT: VARIANT
    }

def _get_datatype(psa):
    # Return the ctypes data type corresponding to the SAFEARRAY's typecode.
    vt = VARTYPE()
    oledll.oleaut32.SafeArrayGetVartype(psa, byref(vt))
    return _VT2CTYPE[vt.value]

def UnpackSafeArray(psa):
    """Unpack a SAFEARRAY into a Python tuple."""
    dim = oledll.oleaut32.SafeArrayGetDim(psa)
    indexes = [_get_lbound(psa, d) for d in range(dim)]
    indexes = (c_long * dim)(*indexes)
    upperbounds = [_get_ubound(psa, d) for d in range(dim)]
    return _get_row(_get_datatype(psa)(), psa, 0, indexes, upperbounds)



if __name__ == "__main__":
    for dim in range(1, 4):

        if dim == 2:
            rgsa = (SAFEARRAYBOUND * 2)()
            rgsa[0].lLbound = 3
            rgsa[0].cElements = 9
            rgsa[1].lLbound = 7
            rgsa[1].cElements = 6

        elif dim == 1:
            rgsa = (SAFEARRAYBOUND * 1)()
            rgsa[0].lLbound = 3
            rgsa[0].cElements = 9

        elif dim == 3:

            rgsa = (SAFEARRAYBOUND * 3)()
            rgsa[0].lLbound = 1
            rgsa[0].cElements = 6
            rgsa[1].lLbound = 2
            rgsa[1].cElements = 5
            rgsa[2].lLbound = 3
            rgsa[2].cElements = 4
        else:
            raise ValueError("dim %d not supported" % dim)
        windll.oleaut32.SafeArrayCreate.restype = POINTER(SAFEARRAY)
        psa = windll.oleaut32.SafeArrayCreate(VT_I4, len(rgsa), rgsa)

        n = 1
        for b in rgsa:
            n *= b.cElements
        print ("%d total elements" % n)

        ptr = POINTER(c_int)()

        oledll.oleaut32.SafeArrayAccessData(psa, byref(ptr))
        array = (c_int * n)(*range(n))
        memmove(ptr, array, sizeof(array))
        oledll.oleaut32.SafeArrayUnaccessData(psa)

        import pprint
        pprint.pprint(UnpackSafeArray(psa))

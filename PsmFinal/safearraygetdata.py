from ctypes import wintypes as wt
import safearraysupport as sf
from ctypes import *
from comtypes.automation import VT_I2
import ctypes as ct
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time
from matplotlib.widgets import SpanSelector
import sys
with open('dll_path.txt', 'r') as file:
    mod_name = file.read().replace('\n', '')
OnLineInterfaceDll = ct.WinDLL(mod_name)
OnLineGetData = OnLineInterfaceDll.OnLineGetData

OnLineGetData.restype = ct.c_int
OnLineGetData.argtypes = (ct.c_long, ct.c_long, ct.POINTER(ct.POINTER(sf.SAFEARRAY)), ct.POINTER(ct.c_long))
OnLineStatus = OnLineInterfaceDll.OnLineStatus
OnLineStatus.argtypes = (ct.c_long, ct.c_long, ct.POINTER(ct.c_long))
oleaut32 = ct.WinDLL("OleAut32.dll")

windll.oleaut32.SafeArrayCreateVectorEx.restype = POINTER(sf.SAFEARRAY)
windll.oleaut32.SafeArrayCreate.restype = POINTER(sf.SAFEARRAY)

SafeArrayCreateVector = oleaut32.SafeArrayCreateVector
SafeArrayCreateVector.argtypes = (ct.c_ushort, wt.LONG, wt.ULONG)
SafeArrayCreateVector.restype = ct.POINTER(sf.SAFEARRAY)
cachey = []
y = []
myodata = []
goniodata = []
semgdata = []
goniodata2 = []
gonioresult = []
def getdata(channel,cachey,samplingrate,gg):

    samples = ct.c_long(0)
    OnLineGetData(channel, samplingrate, gg, ct.byref(samples))
    ggg = sf.UnpackSafeArray(gg)
    data = np.asarray(ggg)
    data = ((data) / 1000)
    cachey.extend(data)
    y = cachey[-20000:]
    return y

def getdataRaw2 (channel,cachey,samplingrate,gg):
    samples = ct.c_long(0)
    OnLineGetData(channel, samplingrate, gg, ct.byref(samples))
    ptr = ct.POINTER(c_void_p)()
    oledll.oleaut32.SafeArrayAccessData(gg, byref(ptr))
    oledll.oleaut32.SafeArrayUnaccessData(gg)
    ggg = sf.UnpackSafeArray(gg)
    data = np.asarray(ggg)
    data = (data*0.0409)
    cachey.extend(data)
    y = cachey[-20000:]
    return y

def getdataRaw1 (channel,cachey,samplingrate,gg):
    samples = ct.c_long(0)
    OnLineGetData(channel, samplingrate, gg, ct.byref(samples))
    ptr = ct.POINTER(c_void_p)()
    oledll.oleaut32.SafeArrayAccessData(gg, byref(ptr))
    oledll.oleaut32.SafeArrayUnaccessData(gg)
    ggg = sf.UnpackSafeArray(gg)
    data = np.asarray(ggg)
    data = (data*0.04426)
    cachey.extend(data)
    y = cachey[-20000:]
    return y

def mainexc(Getsemgdata,Getmyodata,Getgonioresult):
    gg = SafeArrayCreateVector(VT_I2, 0, 0)
    a = ct.c_long(0)
    b = ct.c_long(5)
    c = ct.c_long()
    OnLineStatus(a, b, ct.pointer(c))
    figure, (ax1,ax2,ax3) = plt.subplots(3,figsize=(18, 10))


    def animate(i):
        semg= getdata(0,semgdata,2000,gg)
        gonio = getdataRaw1(2,goniodata,1000,gg)
        myo = getdata(1,myodata,2000,gg)
        gonio2 = getdataRaw2(3, goniodata2, 1000, gg)

        ax1.clear()
        ax2.clear()
        ax3.clear()

        plt.cla()
        ax1.plot(semg,color="red")
        ax2.plot(gonio,color="green")
        ax3.plot(myo,color="blue")
        figure.suptitle('Close this window to stop recording', fontsize=14, fontweight='bold')
        ax1.set_title("SEMG")
        ax2.set_title("Electrogoniometer")
        ax3.set_title("Myometer")

    ani = FuncAnimation(plt.gcf(), animate, interval=1)
    plt.tight_layout()
    plt.show()
    b = ct.c_long(6)
    a = ct.c_long(0)
    c = ct.c_long()
    goniocalculate(goniodata,goniodata2)
    OnLineStatus(a, b, ct.pointer(c))
    Getsemgdata.put(semgdata)
    Getmyodata.put(myodata)
    Getgonioresult.put(gonioresult)


def goniocalculate(goniodata,goniodata2):
    global gonioresult
    if len(goniodata) == len(goniodata2):
        goniodata = np.array(goniodata)
        goniodata2 = np.array(goniodata2)
        gonioresult = goniodata*goniodata + goniodata2*goniodata2
        gonioresult = np.sqrt(gonioresult)

    elif len(goniodata) > len(goniodata2):
        goniodata = goniodata[:len(goniodata2)]
        goniodata = np.array(goniodata)
        goniodata2 = np.array(goniodata2)
        gonioresult = goniodata*goniodata + goniodata2*goniodata2
        gonioresult = np.sqrt(gonioresult)


    elif len(goniodata) < len(goniodata2):
        goniodata2 = goniodata2[:len(goniodata)]
        goniodata = np.array(goniodata)
        goniodata2 = np.array(goniodata2)
        gonioresult = goniodata*goniodata + goniodata2*goniodata2
        gonioresult = np.sqrt(gonioresult)


def GraphSelector(Vsemgdata,Vmyodata,Vgonioresult,text):
    figure, (ax1, ax2, ax3,ax4,ax5,ax6) = plt.subplots(6, figsize=(18, 10),num=text)

    semgdata = Vsemgdata.get()
    myodata = Vmyodata.get()
    gonioresult = Vgonioresult.get()

    Clonesemgdata =semgdata
    Clonemyodata = myodata
    Clonegonioresult=gonioresult

    x1 = list(range(len(semgdata)))
    x2 = list(range(len(gonioresult)))
    x3 = list(range(len(myodata)))

    ax1.plot(x1,semgdata, color="red")
    ax2.plot(x2,gonioresult, color="green")
    ax3.plot(x3,myodata, color="blue")

    ax1.set_title("SEMG")
    ax2.set_title("Electrogoniometer")
    ax3.set_title("Myometer")

    ax4.set_title("SEMG Selection")
    ax5.set_title("Electrogoniometer Selection")
    ax6.set_title("Myometer Selection")

    def onselect1(xmin, xmax):

        nonlocal   Clonesemgdata
        nonlocal   Clonemyodata
        nonlocal   Clonegonioresult

        indmin, indmax = np.searchsorted(x1, (xmin, xmax))
        indmax = min(len(x1) - 1, indmax)


        thisx = x1[indmin:indmax]
        thisy = semgdata[indmin:indmax]
        ax4.plot(thisx, thisy, color="red")
        ax4.set_xlim(thisx[0], thisx[-1])
        figure.canvas.draw()
        Clonesemgdata =  thisy

        thisx = x2[int((indmin/2)):int((indmax/2))]
        thisy = gonioresult[int((indmin/2)):int((indmax/2))]
        ax5.plot(thisx, thisy,color="green")
        ax5.set_xlim(thisx[0], thisx[-1])
        figure.canvas.draw()
        Clonegonioresult = thisy

        thisx = x3[indmin:indmax]
        thisy = myodata[indmin:indmax]
        ax6.plot(thisx, thisy, color="blue")
        ax6.set_xlim(thisx[0], thisx[-1])
        Clonemyodata = thisy




    def onselect2(xmin, xmax):

        nonlocal  Clonesemgdata
        nonlocal   Clonemyodata
        nonlocal   Clonegonioresult

        indmin, indmax = np.searchsorted(x2, (xmin, xmax))
        indmax = min(len(x2) - 1, indmax)


        thisx = x2[indmin:indmax]
        thisy = gonioresult[indmin:indmax]
        ax5.plot(thisx, thisy,color="green")
        ax5.set_xlim(thisx[0], thisx[-1])
        figure.canvas.draw()
        Clonegonioresult = thisy

        thisx = x1[(indmin*2):(indmax*2)]
        thisy = semgdata[(indmin*2):(indmax*2)]
        ax4.plot(thisx, thisy, color="red")
        ax4.set_xlim(thisx[0], thisx[-1])
        figure.canvas.draw()
        Clonesemgdata =  thisy

        thisx = x3[(indmin*2):(indmax*2)]
        thisy = myodata[(indmin*2):(indmax*2)]
        ax6.plot(thisx, thisy, color="blue")
        ax6.set_xlim(thisx[0], thisx[-1])
        Clonemyodata = thisy





    def onselect3(xmin, xmax):
        nonlocal  Clonesemgdata
        nonlocal  Clonemyodata
        nonlocal   Clonegonioresult

        indmin, indmax = np.searchsorted(x3, (xmin, xmax))
        indmax = min(len(x3) - 1, indmax)

        thisx = x3[indmin:indmax]
        thisy = myodata[indmin:indmax]
        ax6.plot(thisx, thisy, color="blue")
        ax6.set_xlim(thisx[0], thisx[-1])
        Clonemyodata = thisy

        thisx = x2[int((indmin/2)):int((indmax/2))]
        thisy = gonioresult[int((indmin/2)):int((indmax/2))]
        ax5.plot(thisx, thisy,color="green")
        ax5.set_xlim(thisx[0], thisx[-1])
        figure.canvas.draw()
        Clonegonioresult = thisy

        thisx = x1[indmin:indmax]
        thisy = semgdata[indmin:indmax]
        ax4.plot(thisx, thisy, color="red")
        ax4.set_xlim(thisx[0], thisx[-1])
        Clonesemgdata =  thisy

        figure.canvas.draw()


    span1 = SpanSelector(ax1, onselect1, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))
    span2 = SpanSelector(ax2, onselect2, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))
    span3 = SpanSelector(ax3, onselect3, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))
    plt.tight_layout()
    plt.show()
    if Clonemyodata != []:
        Vsemgdata.put(Clonesemgdata)
        Vmyodata.put(Clonemyodata)
        Vgonioresult.put(Clonegonioresult)
        print("got assign")
        print(len(gonioresult))
        print(len(Clonemyodata))

    else:
        Vsemgdata.put(semgdata)
        Vmyodata.put(myodata)
        Vgonioresult.put(gonioresult)
        print("no data")



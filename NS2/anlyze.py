import matplotlib.pyplot as plt 
from math import ceil
import os
size = 42

cwndDict2_6 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}
cwndDict1_5 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}
goodputDict1_5 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}
goodputDict2_6 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}
rttDict1_5 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}
rttDict2_6 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}
lostDict1_5 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}
lostDict2_6 = {"newreno": [0] * size, "vegas": [0] * size, "tahoe": [0] * size}

def splitFile(filename):
    lines = []
    file = open(filename, 'r')
    line = file.readline()
    while line:
        lines.append(line.split())
        line = file.readline()
    return lines


def splitCWND(data):
    cwnds1_5 = [-1] * size 
    cwnds2_6 = [-1] * size
    for line in data:
        if "cwnd_" in line:
            if line[1] == '0':
                cwnds1_5[ceil(float(line[0]))] = float(line[6])
            else:
                cwnds2_6[ceil(float(line[0]))] = float(line[6])
    cwnds1_5 = arrange(cwnds1_5, -1)
    cwnds2_6 = arrange(cwnds2_6, -1)
    return cwnds1_5, cwnds2_6

def splitRtt(data):
    rtt1_5 = [-1] * size
    rtt2_6 = [-1] * size
    for line in data:
        if "rtt_" in line:
            if line[1] == '0':
                rtt1_5[ceil(float(line[0]))] = float(line[-1])
            else:
                rtt2_6[ceil(float(line[0]))] = float(line[-1])
    return arrange(rtt1_5, -1), arrange(rtt2_6, -1)


def splitAcks(data): 
    acks1_5 = ['none'] * size
    acks2_6 = ['none'] * size
    for line in data:
        if "ack_" in line:
            if line[1] == '0':
                acks1_5[ceil(float(line[0]))] = float(line[-1])
            else:
                acks2_6[ceil(float(line[0]))] = float(line[-1])
    return arrange(acks1_5, 'none'), arrange(acks2_6, 'none')

def splitLost(data):
    lost1_5 = [-1] * size
    lastlost1_5 = 0
    lost2_6 = [-1] * size
    lastlost2_6 = 0
    for line in data:
        if line[0] == 'd':
            if line[-4][0] =='0':
                lastlost1_5 +=1
                lost1_5[ceil(float(line[1]))] = lastlost1_5
            elif line[-4][0] =='1':
                lastlost2_6 +=1
                lost2_6[ceil(float(line[1]))] = lastlost2_6
    return arrange(lost1_5, -1), arrange(lost2_6, -1)



def arrange(arr, defaultVal):
    for i in range(len(arr)):
        if arr[i] == defaultVal:
            if i != 0:
                arr[i] = arr[i-1]
            else:
                arr[i] = 0
    return arr

def addCwndDatas(newRenoData, vegasData, tahoeData):
    global cwndDict1_5, cwndDict2_6
    newRenoDataCwnd1_5, newRenoDataCwnd2_6 = splitCWND(newRenoData)
    vegasDataCwnd1_5, vegasDataCwnd2_6 = splitCWND(vegasData)
    tahoeDataCwnd1_5, tahoeDataCwnd2_6 = splitCWND(tahoeData)

    for i in range(size):
        cwndDict1_5["newreno"][i] += newRenoDataCwnd1_5[i]
        cwndDict1_5["vegas"][i] += vegasDataCwnd1_5[i]
        cwndDict1_5["tahoe"][i] += tahoeDataCwnd1_5[i]
        cwndDict2_6["newreno"][i] += newRenoDataCwnd2_6[i]
        cwndDict2_6["vegas"][i] += vegasDataCwnd2_6[i]
        cwndDict2_6["tahoe"][i] += tahoeDataCwnd2_6[i]


def addGoodputDatas(newRenoData, vegasData, tahoeData):
    global goodputDict1_5, goodputDict2_6
    newRenoDataAcks1_5, newRenoDataAcks2_6 = splitAcks(newRenoData)
    vegasDataAcks1_5, vegasDataAcks2_6 = splitAcks(vegasData)
    tahoeDataAcks1_5, tahoeDataAcks2_6 = splitAcks(tahoeData)

    for i in range(size):
        goodputDict1_5["newreno"][i] += newRenoDataAcks1_5[i]
        goodputDict1_5["vegas"][i] += vegasDataAcks1_5[i]
        goodputDict1_5["tahoe"][i] += tahoeDataAcks1_5[i]
        goodputDict2_6["newreno"][i] += newRenoDataAcks2_6[i]
        goodputDict2_6["vegas"][i] += vegasDataAcks2_6[i]
        goodputDict2_6["tahoe"][i] += tahoeDataAcks2_6[i]

def addRttDatas(newRenoData, vegasData, tahoeData):
    global rttDict1_5, rttDict2_6
    newRenoDataRtt1_5, newRenoDataRtt2_6 = splitRtt(newRenoData)
    vegasDataRtt1_5, vegasDataRtt2_6 = splitRtt(vegasData)
    tahoeDataRtt1_5, tahoeDataRtt2_6 = splitRtt(tahoeData)

    for i in range(size):
        rttDict1_5["newreno"][i] += newRenoDataRtt1_5[i]
        rttDict1_5["vegas"][i] += vegasDataRtt1_5[i]
        rttDict1_5["tahoe"][i] += tahoeDataRtt1_5[i]
        rttDict2_6["newreno"][i] += newRenoDataRtt2_6[i]
        rttDict2_6["vegas"][i] += vegasDataRtt2_6[i]
        rttDict2_6["tahoe"][i] += tahoeDataRtt2_6[i]

def addLostDatas(newRenoData, vegasData, tahoeData):
    global lostDict1_5, lostDict2_6
    newRenoDataLost1_5, newRenoDataLost2_6 = splitLost(newRenoData)
    vegasDataLost1_5, vegasDataLost2_6 = splitLost(vegasData)
    tahoeDataLost1_5, tahoeDataLost2_6 = splitLost(tahoeData)

    for i in range(size):
        lostDict1_5["newreno"][i] += newRenoDataLost1_5[i]
        lostDict1_5["vegas"][i] += vegasDataLost1_5[i]
        lostDict1_5["tahoe"][i] += tahoeDataLost1_5[i]
        lostDict2_6["newreno"][i] += newRenoDataLost2_6[i]
        lostDict2_6["vegas"][i] += vegasDataLost2_6[i]
        lostDict2_6["tahoe"][i] += tahoeDataLost2_6[i]

def runOnce():
    os.system("ns tahoe_tcp.tcl")
    os.system("ns vegas_tcp.tcl")
    os.system("ns newreno_tcp.tcl")

    tahoeData = splitFile("tahoeTrace.tr")
    vegasData = splitFile("vegasTrace.tr")
    newRenoData = splitFile("newrenoTrace.tr")

    addCwndDatas(newRenoData, vegasData, tahoeData)
    addGoodputDatas(newRenoData, vegasData, tahoeData)
    addRttDatas(newRenoData, vegasData, tahoeData)
    addLostDatas(newRenoData, vegasData, tahoeData)

def run():
    for i in range(10):
        print("run Num #",i+1,)
        runOnce()
    Avrage()


def Avrage():
    global cwndDict1_5, cwndDict2_6, goodputDict1_5, goodputDict2_6
    for key in cwndDict1_5:
        for i in range(size):
            cwndDict1_5[key][i] /= 10
            cwndDict2_6[key][i] /= 10
            goodputDict1_5[key][i] /= 10
            goodputDict2_6[key][i] /= 10
            rttDict1_5[key][i] /= 10
            rttDict2_6[key][i] /= 10
            lostDict1_5[key][i] /= 10
            lostDict2_6[key][i] /= 10

def divide_by_index(arr):
    res = [0] * len(arr)
    res[0] = arr[0]
    for i in range(1, len(arr)):
        res[i] = arr[i] / i
    
    return res




def CwndDiagram():
    global cwndDict1_5, cwndDict2_6
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in cwndDict1_5.keys():
        plt.plot(range(size), cwndDict1_5[key], label=key+'1_5', c=colors[-1])
        colors.pop()
        plt.plot(range(size), cwndDict2_6[key], label=key+'2_6', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("CWND")
    plt.title("CWND/s")
    plt.legend()
    plt.show()



def RttDiagram():
    global rttDict1_5, rttDict2_6
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in rttDict1_5.keys():
        plt.plot(range(size), rttDict1_5[key], label=key+'1_5', c=colors[-1])
        colors.pop()
        plt.plot(range(size), rttDict2_6[key], label=key+'2_6', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("RTT")
    plt.title("RTT/s")
    plt.legend()
    plt.show()

def GPDiagram():
    global goodputDict1_5, goodputDict2_6
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in goodputDict1_5.keys():
        plt.plot(range(size),divide_by_index(goodputDict1_5[key]), label=key+'1_5', c=colors[-1])
        colors.pop()
        plt.plot(range(size), divide_by_index(goodputDict2_6[key]), label=key+'2_6', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("Goodput")
    plt.title("Goodput/s")
    plt.legend()
    plt.show()

def LossDiagram():
    global lostDict1_5, lostDict2_6
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in lostDict1_5.keys():
        plt.plot(range(size), divide_by_index(lostDict1_5[key]), label=key+'1_5', c=colors[-1])
        colors.pop()
        plt.plot(range(size), divide_by_index(lostDict2_6[key]), label=key+'2_6', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("Lost")
    plt.title("Lost/s")
    plt.legend()
    plt.show()


run()
CwndDiagram()
RttDiagram()
GPDiagram()
LossDiagram()
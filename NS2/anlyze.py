import matplotlib.pyplot as plt 
from math import ceil
import os

cwnfDict15 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}
cwnfDict04 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}
goodputDict04 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}
goodputDict15 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}
rttDict04 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}
rttDict15 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}
lostDict04 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}
lostDict15 = {"newreno": [0] * 1001, "vegas": [0] * 1001, "tahoe": [0] * 1001}

def splitFile(filename):
    Lines = []
    file = open(filename, 'r')
    line = file.readline()
    while line:
        lines.append(line.split())
        line = file.readline()
    return lines

def adjustArray(arr, defaultVal):
    for i in range(len(arr)):
        if arr[i] == defaultVal:
            arr[i] = arr[i-1] if i != 0 else 0
    return arr

def splitCWND(data):
    cwnds04 = [-1] * 1001
    cwnds15 = [-1] * 1001
    for line in data:
        if "cwnd" in line:
            indexes = [0.6]
            if line[1] == '0':
                cwnds04[ceil(float(line[0]))] = float(line[6])
            else:
                cwnds15[ceil(float(line[0]))] = float(line[6])
    cwnds04 = adjustArray(cwnds04, -1)
    cwnds15 = adjustArray(cwnds15, -1)
    return cwnds04, cwnds15


def splitAcks(data):
    acks04 = ['none'] * 1001
    acks15 = ['none'] * 1001
    for line in data:
        if "ack" in line:
            if line[1] == '0':
                acks04[ceil(float(line[0]))] = float(line[-1])
            else:
                acks15[ceil(float(line[0]))] = float(line[-1])
    return adjustArray(acks04, 'none'), adjustArray(acks15, 'none')

def splitLost(data):
    lost04 = [-1] * 1001
    lastlost04 = 0
    lost15 = [-1] * 1001
    lastlost15 = 0
    for line in data:
        if "lost" in line:
            indexes = [0.6]
            if line[1] == '0':
                lost04[ceil(float(line[0]))] = float(line[6]) - lastlost04
                lastlost04 = float(line[6])
            else:
                lost15[ceil(float(line[0]))] = float(line[6]) - lastlost15
                lastlost15 = float(line[6])

    return adjustArray(lost04, -1), adjustArray(lost15, -1)

def splitRtt(data):
    rtt04 = [-1] * 1001
    rtt15 = [-1] * 1001
    for line in data:
        if "rtt" in line:
            if line[1] == '0':
                rtt04[ceil(float(line[0]))] = float(line[-1])
            else:
                rtt15[ceil(float(line[0]))] = float(line[-1])
    return adjustArray(rtt04, -1), adjustArray(rtt15, -1)

def addCwndDatas(newRenoData, vegasData, tahoeData):
    global cwndDict04, cwndDict15
    newRenoDataCwnd04, newRenoDataCwnd15 = splitCWND(newRenoData)
    vegasDataCwnd04, vegasDataCwnd15 = splitCWND(vegasData)
    tahoeDataCwnd04, tahoeDataCwnd15 = splitCWND(tahoeData)

    for i in range(1001):
        cwndDict04["newreno"][i] += newRenoDataCwnd04[i]
        cwndDict04["vegas"][i] += vegasDataCwnd04[i]
        cwndDict04["tahoe"][i] += tahoeDataCwnd04[i]
        cwndDict15["newreno"][i] += newRenoDataCwnd15[i]
        cwndDict15["vegas"][i] += vegasDataCwnd15[i]
        cwndDict15["tahoe"][i] += tahoeDataCwnd15[i]


def addGoodputDatas(newRenoData, vegasData, tahoeData):
    global goodputDict04, goodputDict15
    newRenoDataAcks04, newRenoDataAcks15 = splitAcks(newRenoData)
    vegasDataAcks04, vegasDataAcks15 = splitAcks(vegasData)
    tahoeDataAcks04, tahoeDataAcks15 = splitAcks(tahoeData)

    for i in range(1001):
        goodputDict04["newreno"][i] += newRenoDataAcks04[i]
        goodputDict04["vegas"][i] += vegasDataAcks04[i]
        goodputDict04["tahoe"][i] += tahoeDataAcks04[i]
        goodputDict15["newreno"][i] += newRenoDataAcks15[i]
        goodputDict15["vegas"][i] += vegasDataAcks15[i]
        goodputDict15["tahoe"][i] += tahoeDataAcks15[i]

def addRttDatas(newRenoData, vegasData, tahoeData):
    global rttDict04, rttDict15
    newRenoDataRtt04, newRenoDataRtt15 = splitRtt(newRenoData)
    vegasDataRtt04, vegasDataRtt15 = splitRtt(vegasData)
    tahoeDataRtt04, tahoeDataRtt15 = splitRtt(tahoeData)

    for i in range(1001):
        rttDict04["newreno"][i] += newRenoDataRtt04[i]
        rttDict04["vegas"][i] += vegasDataRtt04[i]
        rttDict04["tahoe"][i] += tahoeDataRtt04[i]
        rttDict15["newreno"][i] += newRenoDataRtt15[i]
        rttDict15["vegas"][i] += vegasDataRtt15[i]
        rttDict15["tahoe"][i] += tahoeDataRtt15[i]
def addLostDatas(newRenoData, vegasData, tahoeData):
    global lostDict04, lostDict15
    newRenoDataLost04, newRenoDataLost15 = splitLost(newRenoData)
    vegasDataLost04, vegasDataLost15 = splitLost(vegasData)
    tahoeDataLost04, tahoeDataLost15 = splitLost(tahoeData)

    for i in range(1001):
        lostDict04["newreno"][i] += newRenoDataLost04[i]
        lostDict04["vegas"][i] += vegasDataLost04[i]
        lostDict04["tahoe"][i] += tahoeDataLost04[i]
        lostDict15["newreno"][i] += newRenoDataLost15[i]
        lostDict15["vegas"][i] += vegasDataLost15[i]
        lostDict15["tahoe"][i] += tahoeDataLost15[i]

def runOneEpoch():
    os.system("ns tahoe_tcp.tcl")
    os.system("ns vegas_tcp.tcl")
    os.system("ns newreno_tcp.tcl")

    newRenoData = splitFile("newrenoTrace.tr")
    vegasData = splitFile("vegasTrace.tr")
    tahoeData = splitFile("tahoeTrace.tr")

    addCwndDatas(newRenoData, vegasData, tahoeData)
    addGoodputDatas(newRenoData, vegasData, tahoeData)
    addRttDatas(newRenoData, vegasData, tahoeData)
    addLostDatas(newRenoData, vegasData, tahoeData)

def calcAvgVars():
    global cwndDict04, cwndDict15, goodputDict04, goodputDict15, rttDict04, rttDict15, lostDict04, lostDict15
    for key in cwndDict04:
        for i in range(1001):
            cwndDict04[key][i] /= 10
            cwndDict15[key][i] /= 10
            goodputDict04[key][i] /= 10
            goodputDict15[key][i] /= 10
            rttDict04[key][i] /= 10
            rttDict15[key][i] /= 10
            lostDict04[key][i] /= 10
            lostDict15[key][i] /= 10

def run():
    for i in range(10):
        print("Epoch: ", i, " started")
        runOneEpoch()
    calcAvgVars()

def analyzeCWND():
    global cwndDict04, cwndDict15
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in cwndDict04:
        plt.plot(range(1001), cwndDict04[key], label=key+'04', c=colors[-1])
        colors.pop()
        plt.plot(range(1001), cwndDict15[key], label=key+'15', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("CWND")
    plt.title("CWND/s")
    plt.legend()
    plt.show()



def analyzeRTT():
    global rttDict04, rttDict15
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in rttDict04:
        plt.plot(range(1001), rttDict04[key], label=key+'04', c=colors[-1])
        colors.pop()
        plt.plot(range(1001), rttDict15[key], label=key+'15', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("RTT")
    plt.title("RTT/s")
    plt.legend()
    plt.show()

def analyzeGoodput():
    global goodputDict04, goodputDict15
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in goodputDict04:
        plt.plot(range(1001), goodputDict04[key], label=key+'04', c=colors[-1])
        colors.pop()
        plt.plot(range(1001), goodputDict15[key], label=key+'15', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("Goodput")
    plt.title("Goodput/s")
    plt.legend()
    plt.show()

def analyzeLost():
    global lostDict04, lostDict15
    colors = ['c', 'm', 'y', 'g', 'b', 'r']
    for key in lostDict04:
        plt.plot(range(1001), lostDict04[key], label=key+'04', c=colors[-1])
        colors.pop()
        plt.plot(range(1001), lostDict15[key], label=key+'15', c=colors[-1])
        colors.pop()

    plt.xlabel("Time")
    plt.ylabel("Lost")
    plt.title("Lost/s")
    plt.legend()
    plt.show()

def derivate(arr):
    arr2 = [0] * len(arr)
    for i in range(1, len(arr)):
        arr2[i] = arr[i] / i
    arr2[0] = arr[0]
    return arr2

def diffrence(arr1):
    arr2 = [0] * len(arr1)
    for i in range(1, len(arr1)):
        arr2[i] = arr1[i] - arr1[i-1]
    arr2[0] = arr1[0]
    return arr2


run()
analyzeCWND()
analyzeRTT()
analyzeGoodput()
analyzeLost()
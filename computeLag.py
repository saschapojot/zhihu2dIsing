import pickle
import numpy as np
import random
from copy import deepcopy
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path


# randseed = 198
# random.seed(randseed)

N = 20  # length of one direction
J = 1

T = 0.1
beta = 1 / T
part=0
# init s
tInitStart = datetime.now()
sVals = [-1, 1]
sCurr = np.zeros((N, N), dtype=float)
for i in range(0, N):
    for j in range(0, N):
        sCurr[i, j] = sVals[random.randint(0, 1)]

procNum=48
# def energyAtab(ab):
#     a, b = ab
#     sLeft = sCurr[a, (b - 1) % N]
#     sRight = sCurr[a, (b + 1) % N]
#     sUp = sCurr[(a - 1) % N, b]
#     sDown = sCurr[(a + 1) % N, b]
#     return -J / 2 * sCurr[a, b] * (sLeft + sRight + sUp + sDown)
# pool0=Pool(procNum)
# indsAll=[[a,b] for a in range(0,N) for b in range(0,N)]
# retEAll=pool0.map(energyAtab,indsAll)
# ECurr=np.sum(retEAll)
tInitEnd=datetime.now()
print("init time: ",tInitEnd-tInitStart)

tMCStart = datetime.now()
flipNum = 0
notFlipNum = 0
maxStep = 100
totalLoop=maxStep*N**2

def rectangularOutput(arr):
    """

    :param arr: matrix
    :return: write in rectangular array excluding [[and ]]
    """
    outArrStr="\n"
    for row in arr:
        rs=" ".join(map(str,row))
        outArrStr+=rs+"\n"
    return outArrStr

class computationData:  # holding computational results to be dumped using pickle
    def __init__(self):
        self.sAll = []  # list
        self.E=[]
# indsAll=[[a,b] for a in range(0,N) for b in range(0,N)]
print("T="+str(T))
# print("randseed="+str(randseed))
record = computationData()
for tau in range(0, totalLoop):
    # print("step " + str(tau))
    # tOneMCStepStart = datetime.now()

    # flip s
    a = random.randint(0, N - 1)
    b = random.randint(0, N - 1)
    sNext=deepcopy(sCurr)
    sLeft = sNext[a, (b - 1) % N]
    sRight = sNext[a, (b + 1) % N]
    sUp = sNext[(a - 1) % N, b]
    sDown = sNext[(a + 1) % N, b]

    DeltaE = 2 * J * sNext[a, b] * (sLeft + sRight + sUp + sDown)
    # print("Delta E=" + str(DeltaE))
    if DeltaE <= 0:
        # print("Delta E<=0")
        sNext[a, b] *= -1
        # print("flipped")
        flipNum += 1
    else:
        r = random.random()
        # print("r=" + str(r))
        # print("exp(-beta*Delta E)=" + str(np.exp(-beta * DeltaE)))
        if r < np.exp(-beta * DeltaE):
            sNext[a, b] *= -1
            # print("flipped")
            flipNum += 1
        else:
            # print("not flipped")
            notFlipNum += 1


    sCurr=deepcopy(sNext)
    # ECurr+=DeltaE
    record.sAll.append(sCurr)
    # record.E.append(ECurr)
    # def energyAtab(ab):
    #     a,b=ab
    #     sLeft = sCurr[a, (b - 1) % N]
    #     sRight = sCurr[a, (b + 1) % N]
    #     sUp = sCurr[(a - 1) % N, b]
    #     sDown = sCurr[(a + 1) % N, b]
    #     return -J/2*sCurr[a,b]*(sLeft+sRight+sUp+sDown)
    #
    # pool0=Pool(procNum)
    # retEAll=pool0.map(energyAtab,indsAll)
    # ETot=np.sum(retEAll)
    # record.E.append(ETot)
    # print("sCurr=" + str(rectangularOutput(sCurr)))
    # tOneMCStepEnd = datetime.now()
    # print("one step MC :", tOneMCStepEnd - tOneMCStepStart)
    # print("=====================================")
    if tau % 5000 == 0:
        print("flip " + str(tau))

tMCEnd = datetime.now()
print("MC time: ", tMCEnd - tMCStart)
print("flip num: " + str(flipNum))
print("no flip num: " + str(notFlipNum))
###place holder
###place holder
outPklFileName = "T" + str(T) + "step" + str(maxStep) + "out.pkl"
with open(outPklFileName, "wb") as fptr:
    pickle.dump(record, fptr, pickle.HIGHEST_PROTOCOL)
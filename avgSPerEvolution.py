import pickle
# from copy import deepcopy
import numpy as np
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import glob
import re

# this script computes the evolution of  average of s over the whole lattice through the MC process

class computationData:  # holding computational results to be dumped using pickle
    def __init__(self):
        self.sAll = []  # list
        self.E=[]

part=0
pklFileNames=[]
TValsAll=[]
inDir="./part"+str(part)+"/"
for file in glob.glob(inDir+"*.pkl"):
    pklFileNames.append(file)
    # search T value
    matchT = re.search(r"T(-?\d+(\.\d+)?)J", file)
    if matchT:
        TValsAll.append(matchT.group(1))


val0=(len(TValsAll)-len(pklFileNames))**2
if val0!=0:
    raise ValueError("unequal length.")

def str2float(valList):
    ret=[float(strTmp) for strTmp in valList]
    return ret

TValsAll=str2float(TValsAll)

#sort temperatures and files
T_inds=np.argsort(TValsAll)
pklFileNames=[pklFileNames[ind] for ind in T_inds]
TValsAll=[TValsAll[ind] for ind in T_inds]
figDir=inDir+"/sEvo/"
Path(figDir).mkdir(parents=True, exist_ok=True)
tStart=datetime.now()
for i in range(0,len(pklFileNames)):
    TTmp = TValsAll[i]
    inPklFileName = pklFileNames[i]
    t1loopStart = datetime.now()
    with open(inPklFileName, "rb") as fptr:
        record = pickle.load(fptr)
    sAllMean=np.mean(np.array(record.sAll),axis=(1,2)) #mean of s for each configuration
    #plt
    fig,ax=plt.subplots()
    ax.plot(sAllMean,color="black")
    ax.set_ylabel("avg of s in whole lattice")
    ax.set_xlabel("MC step")
    ax.set_title("$T=$" + str(TTmp))
    plt.savefig(figDir + "rec" + str(i) + "Temp" + str(TTmp) + ".png")
    plt.close()
    t1loopEnd = datetime.now()
    print("loop time: ", t1loopEnd - t1loopStart)

tEnd=datetime.now()

print("time: ",tEnd-tStart)
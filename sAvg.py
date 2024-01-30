import pickle
# from copy import deepcopy
import numpy as np
from datetime import datetime

import matplotlib.pyplot as plt
import glob
import re
from multiprocessing import Pool
#This script computes avgerage value of s
#This script computes magnetic susceptibility
#This script computes specific heat

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
    matchJ=re.search(r"J(-?\d+(\.\d+)?)rand",file)
    if matchJ:
        J=float(matchJ.group(1))

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

tPltStart=datetime.now()
sAvgAll=[]
chiValAll=[]
specificHeatAll=[]

lastNum=100000#use the last lastNum configurations
separation=130#separation of the used configurations

for i in range(0,len(pklFileNames)):
    inPklFileName = pklFileNames[i]
    tLoadStart = datetime.now()
    with open(inPklFileName, "rb") as fptr:
        record = pickle.load(fptr)
    tLoadEnd = datetime.now()
    print("loading time: ", tLoadEnd - tLoadStart)
    sLast = np.array(record.sAll[-lastNum::separation])
    smTmp=np.mean(sLast,axis=(1,2))# mean spin for each configuration
    sVal = np.mean(np.abs(smTmp))
    sAvgAll.append(sVal)
    ##average of spin over configurations
    meanS = np.mean(smTmp)
    # square of avg spin for one configuration
    sSquared = smTmp ** 2
    meanS2 = np.mean(sSquared)
    T = TValsAll[i]
    chiTmp = (meanS2 - meanS ** 2) / T
    chiValAll.append(chiTmp)

    # sLastList=record.sAll[-lastNum::separation]
    # print(type(sLast[0]))
    def energy(spins):
        return -J * (np.sum(spins[:-1, :] * spins[1:, :]) + np.sum(spins[:, :-1] * spins[:, 1:])) \
            - J * (np.sum(spins[0, :] * spins[-1, :]) + np.sum(spins[:, 0] * spins[:, -1]))
    procNum=48
    pool0=Pool(procNum)
    EretAll=pool0.map(energy,sLast)
    EretAll=np.array(EretAll)


    # specific heat

    meanE = np.mean(EretAll)
    EAvgLast2 = EretAll ** 2
    meanE2 = np.mean(EAvgLast2)
    CTmp = (meanE2 - meanE ** 2) / T ** 2
    specificHeatAll.append(CTmp)


#plot <s> vs T
fig,ax=plt.subplots()
ax.scatter(TValsAll,sAvgAll,color="black")
plt.xlabel("$T$")
plt.ylabel("<s>")
plt.title("Temperature from "+str(TValsAll[0])+" to "+str(TValsAll[-1]))
# ax.spines['left'].set_position('zero')
# ax.spines['bottom'].set_position('zero')

# Hide top and right spines
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
plt.yticks([0,0.2,0.4,0.6,0.8,1])
ax.tick_params(axis='both', which='major', labelsize=6)
plt.savefig(inDir+"T"+str(TValsAll[0])+"toT"+str(TValsAll[-1])+"sAvg.png")
plt.close()


# plot chi vs T
fig,ax=plt.subplots()
ax.scatter(TValsAll,chiValAll,color="red")
plt.title("Temperature from "+str(TValsAll[0])+" to "+str(TValsAll[-1]))
plt.xlabel("$T$")
plt.ylabel("$\chi$")
# ax.spines['left'].set_position('zero')
# ax.spines['bottom'].set_position('zero')

# Hide top and right spines
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
ax.tick_params(axis='both', which='major', labelsize=6)
plt.savefig(inDir+"T"+str(TValsAll[0])+"toT"+str(TValsAll[-1])+"Chi.png")
plt.close()


#plot C vs T
fig,ax=plt.subplots()
ax.scatter(TValsAll,specificHeatAll,color="blue")
plt.title("Temperature from "+str(TValsAll[0])+" to "+str(TValsAll[-1]))
plt.xlabel("$T$")
plt.ylabel("$C$")
# ax.spines['left'].set_position('zero')
# ax.spines['bottom'].set_position('zero')

# Hide top and right spines
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
ax.tick_params(axis='both', which='major', labelsize=6)
plt.savefig(inDir+"T"+str(TValsAll[0])+"toT"+str(TValsAll[-1])+"specificHeat.png")



tPltEnd=datetime.now()
print("time: ",tPltEnd-tPltStart)

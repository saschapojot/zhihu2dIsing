
import re
from pathlib import Path

#this script generates MCMC computing scripts as well as bash files for submitting jobs

lagFileName="computeLag"
suffix=".py"
part=0

TemperaturesAll=[1+0.1*n  for n in range(0,21)]
randSeedAll=[1890]
fileIn=open(lagFileName+suffix,"r")

contents=fileIn.readlines()
fileIn.close()
lineTemperature=0#the line corresponding to T=xxxxx (temperature)
lineRandSeed=0# random seed
lineMaxStep=0# loop numbers in first mc
linePart=0

for l in range(0,len(contents)):
    line=contents[l]
    if re.findall("^T\s*=\s*(-?\d+(\.\d+)?)",line):
        lineTemperature=l
        # print(lineTemperature)
    if re.findall("^randseed\s*=\s*\d+",line):
        lineRandSeed=l
        # print(lineRandSeed)
    if re.findall("^maxStep\s*=\s*\d+",line):
        lineMaxStep=l
    if re.findall("^part\s*=\d+",line):
        linePart=l

#generate computing files
setMaxStep=500
counter=0
for TVal in TemperaturesAll:
    for rs in randSeedAll:
        contents[lineTemperature] = "T=" + str(TVal) + "\n"
        contents[lineRandSeed] = "randseed =(" + str(rs) + ")\n"
        contents[linePart] = "part=" + str(part) + "\n"
        contents[lineMaxStep] = "maxStep=" + str(setMaxStep) + "\n"
        contents[-5] = 'outDir="./part"+str(part)+"/"\n'
        contents[-4] = 'Path(outDir).mkdir(parents=True, exist_ok=True)\n'
        contents[-3] = 'outPklFileName=outDir+"T"+str(T)+"J"+str(J)' + '+"randseed"+str(' + str(
            rs) + ')+"loop"+str(totalLoop)+"part"+str(' + str(
            part) + ')+"out.pkl"\n'
        outFileName = "computeLag" + str(counter) + "part" + str(part) + "randseed" + str(rs) + ".py"
        fileOut = open(outFileName, "w+")
        for oneline in contents:
            fileOut.write(oneline)
        fileOut.close()
        counter += 1

bashDir="./lagBash/"
Path(bashDir).mkdir(parents=True, exist_ok=True)
#generate bash files
counter=0
for TVal in TemperaturesAll:
    for rs in randSeedAll:
        bashContents = []
        bashContents.append("#!/bin/bash\n")
        bashContents.append("#SBATCH -n 12\n")
        bashContents.append("#SBATCH -N 1\n")
        bashContents.append("#SBATCH -t 0-40:00\n")
        bashContents.append("#SBATCH -p CLUSTER\n")
        bashContents.append("#SBATCH --mem=40GB\n")
        bashContents.append("#SBATCH -o outlag" + str(counter) + ".out\n")
        bashContents.append("#SBATCH -e outlag" + str(counter) + ".err\n")
        bashContents.append("cd /home/cywanag/liuxi/Documents/pyCode/zhihu2dIsing\n")
        bashContents.append(
            "python3 computeLag" + str(counter) + "part" + str(part) + "randseed" + str(rs) + ".py > part" + str(
                part) + "rec" + str(
                counter) + "Temp" + str(TVal) + ".txt\n")
        bsFileName = bashDir+"lag" + str(counter) + ".sh"
        fbsTmp = open(bsFileName, "w+")
        for oneline in bashContents:
            fbsTmp.write(oneline)
        fbsTmp.close()
        counter += 1
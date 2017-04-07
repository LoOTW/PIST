"Pour afficher les résultats de loss.txt"
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
def file2list(name):
    with open(name+".txt") as f:
        file = f.read().splitlines()
    l=[]
    file = str(file[0])
    file = file[1:len(file)-1]
    file = file.split(", ")

    for i in range(1,len(file)-1):

        l.append(float(file[i]))
    return l



def file2listGliss(name):
    gliss = 25
    with open(name + ".txt") as f:
        file = f.read().splitlines()
    l = []
    file = str(file[0])
    file = file[1:len(file) - 1]
    file = file.split(", ")

    initialMean=[]
    for i in range(gliss):
        initialMean.append(float(file[i]))
        l.append(np.mean(initialMean))
    for i in range(1 + gliss, len(file) - 1):
        temp = []
        for j in range(gliss):
            temp.append(float(file[i - j]))
        l.append(np.mean(temp))
    return l

def file2listGlissStd(name):
    gliss = 25
    with open(name + ".txt") as f:
        file = f.read().splitlines()
    l = []
    file = str(file[0])
    file = file[1:len(file) - 1]
    file = file.split(", ")
    std=[]
    for i in range(gliss):
        std.append(float(file[i]))

    initialMean=[]
    for i in range(gliss):
        initialMean.append(float(file[i]))
        l.append(np.mean(initialMean)+np.std(std))
    for i in range(1 + gliss, len(file) - 1):
        temp = []
        for j in range(gliss):
            temp.append(float(file[i - j]))
        l.append(np.mean(temp) + np.std(temp))
    return l



loss = file2list("loss")
epsilon = file2list("epsilon")
victoires = file2list("victoires")
defaites = file2list("defaites")
ratiosG = file2listGliss("ratios")
pasAvantMortsG=file2listGliss("pasAvantMort")
lossG = file2listGlissStd("loss")
victoiresG = file2listGliss("victoires")
defaitesG = file2listGliss("defaites")
plt.figure(1)

plt.subplot(331)
plt.title('epsilon')
plt.plot(epsilon)

plt.subplot(332)
plt.title('loss')
plt.yscale('log')
plt.plot(loss)

plt.subplot(333)
plt.title('loss MG majorée')
plt.yscale('log')
plt.plot(lossG)


plt.subplot(334)
plt.title('victoires')
plt.plot(victoires)

plt.subplot(335)
plt.title('defaites')
plt.plot(defaites)

plt.subplot(336)
plt.title('ratio MG')
plt.plot(ratiosG)

plt.subplot(337)
plt.title('victoires MG')
plt.plot(victoiresG)

plt.subplot(338)
plt.title('defaites MG')
plt.plot(defaitesG)

plt.subplot(339)
plt.title('step before death MG')
plt.yscale('log')
plt.plot(pasAvantMortsG)


plt.tight_layout()
plt.show()



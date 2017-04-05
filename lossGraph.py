"Pour afficher les résultats de loss.txt"

import matplotlib.pyplot as mlt
from pathlib import Path

with open("loss.txt") as f:
    file = f.read().splitlines()
l=[]
file = str(file[0])
file = file[1:len(file)-1]
file = file.split(", ")

for i in range(1,len(file)-1):
   l.append(float(file[i]))
   
"ECHELLE LOGARITHIQUE"
#mlt.xscale('log')
#mlt.yscale('log')
mlt.plot(file)
mlt.show()
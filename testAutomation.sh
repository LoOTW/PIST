#!/bin/bash

read -p 'Nombre de tests à effectuer : ' nbTest


for i in `seq 1 $nbTest`;
do
	echo "Test $i"
	read -p 'Alpha :' alphaTab[i]
done

for i in `seq 1 $nbTest`;
do
	echo "Test $i"
	read -p 'gamma :' gammaTab[i]
done

for i in `seq 1 $nbTest`;
do
	echo "Test $i"
	read -p 'Première couche :' neur1Tab[i]
done

for i in `seq 1 $nbTest`;
do
	echo "Test $i"
	read -p 'Deuxième couche :' neur2Tab[i]
done

for i in `seq 1 $nbTest`;
do
	mkdir "Test$i"
	cp snakeNeural.py "Test$i/"
	cd "Test$i/"
	x-terminal-emulator -e python3 "snakeNeural.py" ${alphaTab[i]} ${gammaTab[i]} ${neur1Tab[i]} ${neur2Tab[i]}
	cd ".."
done

echo ${alphaTab[*]}

# echo $nbTest
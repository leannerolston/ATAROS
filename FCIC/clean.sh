#!/bin/bash

for f in `ls *.txt`
do
	base=${f}
	echo $base
	ofile="${base/.txt/}_cleaned.txt" 
	echo $ofile
	python3 ../software/cleanTextGridOutput.py $f > ${ofile}
done

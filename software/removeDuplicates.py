#!/usr/bin/env
# -*- coding: utf-8 -*-

#Tryingto find idential spurts with different stance labels.

import os, sys
import string

dir = sys.argv[1]

files = [f for f in os.listdir(dir) if f.endswith("_cleaned.txt")]

text_comparator = {}
#txt[stance][txt] with task somehow in there.

for f in files:
	with open(os.path.join(dir, f)) as inp:
		for line in inp:
			line = line.strip("\n")
			tokens = line.split("\t")

			stance = tokens[0]
			task = tokens[1]
			text = tokens[2]

			#Remove punctuation and -
			trimmed_text = [l for l in text if l not in string.punctuation]
			trimmed_text = ''.join([l for l in trimmed_text if l != "-"])


			if trimmed_text not in text_comparator:
				text_comparator[trimmed_text] = {}

			if stance not in text_comparator[trimmed_text]:
				text_comparator[trimmed_text][stance] = []

			tup = task, text
			text_comparator[trimmed_text][stance].append(tup)

dupes = open("ATAROS_Duplicates.txt", "w")
newdata = open("ATAROS_minus_Duplicates.txt", "w")


for text in text_comparator:

	stances = text_comparator[text]

	if len(stances) > 1:
		#print(text, end="\t")
		st = list(stances.keys())
		#print(st)
		dupes.write(text)
		dupes.write("\t")
		dupes.write(' '.join(st))
		dupes.write("\n")

	else:
		for s in stances:
			d = stances[s]

			for item in d:

				newdata.write(s)
				newdata.write("\t")

				task = item[0]
				txt = item[1]

				newdata.write(task)
				newdata.write("\t")

				newdata.write(txt)
				newdata.write("\n")


dupes.close()
newdata.close()




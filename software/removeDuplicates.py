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
			#trimmed_text = [l for l in text if l not in string.punctuation]
			#trimmed_text = ''.join([l for l in trimmed_text if l != "-"])
			trimmed_text = ' '.join(text.split())

			if trimmed_text not in text_comparator:
				text_comparator[trimmed_text] = {}

			if stance not in text_comparator[trimmed_text]:
				text_comparator[trimmed_text][stance] = []

			text_comparator[trimmed_text][stance].append(task)

dupes = open("ATAROS_Duplicates.txt", "w")
dupes.write("Text\tStances\tTasks\tCount\n")
newdata = open("ATAROS_minus_Duplicates.txt", "w")


for text in text_comparator:

	stances = text_comparator[text]

	if len(stances) > 1:
		#print(text, end="\t")
		st = list(stances.keys())
		tasks = [text_comparator[text][s] for s in st]

		tsk = []
		for t in tasks:
			tsk.extend(t)

		tasks = list(set(tsk))

		dupes.write(text)
		dupes.write("\t")
		dupes.write(' '.join(st))
		dupes.write("\t")
		dupes.write(' '.join(tasks))
		dupes.write("\t")
		dupes.write(str(len(tsk)))
		dupes.write("\n")

	else:
		for s in stances:
			task = text_comparator[text][s]


			for t in task:
				newdata.write(s)
				newdata.write("\t")

				newdata.write(t)
				newdata.write("\t")

				newdata.write(text)
				newdata.write("\n")



dupes.close()
newdata.close()




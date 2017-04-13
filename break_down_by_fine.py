#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys

def printLine(speaker, task, stance, fine_annotation, sentence):
	#make sure tag doesn't have a #:
	fine_annotation = fine_annotation.replace("#", "")

	for tag in fine_annotation:
		print(speaker, end="\t")
		print(task, end="\t")
		print(tag, end="\t")
		print(stance, end="\t")
		print(sentence)

with open(sys.argv[1]) as inp:
	for line in inp:
		line = line.strip()

		tokens = line.split("\t")

		if len(tokens) < 5:
			continue

		speaker = tokens[0]
		task = tokens[1]
		#stance = tokens[2]
		stance = tokens[2].replace("+", "").replace("-", "").replace("X", "").replace("x", "")
		transcription = tokens[3]
		fine = tokens[4]

		#TODO: Weed out stances
		if not stance:
			continue

		wds = [l.split(":") for l in fine.split()]

		wds_with_tags = [l for l, x in enumerate(wds) if len(x) > 1 and x[1].strip()]



		if len(wds_with_tags) < 1:
			continue

		sentence = ""
		fine_annotation = ""

		for i in range(len(wds_with_tags)):
			pair = wds[wds_with_tags[i]]
			wd = pair[0].lower()
			tag = pair[1]

			if i == 0:
				fine_annotation = tag
				sentence += wd

			elif tag != fine_annotation:
				#We've hit upon a new tag and should print out the previous:
				printLine(speaker, task, stance, fine_annotation, sentence)
				sentence = ""
				fine_annotation = tag
				sentence += wd
			else:
				sentence += wd

			if i < len(wds_with_tags) - 1:
				sentence += " "

		else:
			#end of list, so print out sensense:
			printLine(speaker, task, stance, fine_annotation, sentence)








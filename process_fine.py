#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, collections

cats = sys.argv[1]
file = sys.argv[2]

labels = {}
#l[wd] = [cat1, cat2]

ctgry = []

with open(cats) as inp:
	data = [l.strip() for l in inp if l]

for d in data:

	if not d:
		continue

	tokens = d.split("\t")

	category = tokens[0]

	ctgry.append(category)

	words = tokens[1].split()

	for w in words:
		if w not in labels:
			labels[w] = []

		labels[w].append(category)

trans_idx = open("transciption_index.txt", "w")

headerprint = 0

with open(file) as inp:
	for line in inp:
		line = line.strip()

		if not line:
			continue

		tokens = line.split("\t")

		if len(tokens) < 5:
			continue

		speaker = tokens[0]
		task = tokens[1]
		stance = tokens[2].replace("+", "").replace("-", "").replace("X", "").replace("x", "")
		transcription = tokens[3]
		fine = tokens[4]

		if not stance:
			continue

		#find punctuation:
		comma = [l for l, x in enumerate(transcription) if x == ","]
		period = [l for l, x in enumerate(transcription) if x == "."]
		qmark = [l for l, x in enumerate(transcription) if x == "?"]
		exmark = [l for l, x in enumerate(transcription) if x == "!"]

		#speaker, task, stance, len(fine), len(categories)
		stats = collections.OrderedDict()
		stats['speaker'] = speaker
		stats['task'] = task
		stats['stance'] = stance
		stats['o'] = 0
		stats['s'] = 0
		stats['c'] = 0
		stats['a'] = 0
		stats['d'] = 0
		stats['r'] = 0
		stats['f'] = 0
		stats['t'] = 0
		stats['e'] = 0
		stats['i'] = 0
		stats['x'] = 0
		stats['b'] = 0
		stats['period'] = 0
		stats['comma'] = 0
		stats['questionmark'] = 0
		stats['exclamationmark'] = 0
		stats['pronoun'] = 0
		stats['ipron'] = 0
		stats['ppron'] = 0
		stats['singPPron'] = 0
		stats['plurPPron'] = 0
		stats['1stPPron'] = 0
		stats['2ndPPron'] = 0
		stats['3rdPPron'] = 0
		stats['defArt'] = 0
		stats['indefArt'] = 0
		stats['function'] = 0
		stats['prep'] = 0
		stats['conj'] = 0
		stats['filler'] = 0
		stats['nonflu'] = 0
		stats['swear'] = 0
		stats['tentat'] = 0
		stats['differ'] = 0
		stats['discrep'] = 0
		stats['certain'] = 0

		if headerprint < 1:
			for s in stats:
				print(s, end="\t")
			print()

			headerprint += 1


		#attempt #1: fine annotation as another feature
		#1a - binary features
		#1b - real valued

		trans_idx.write(transcription)
		trans_idx.write("\n")

		###BINARY FEATURES###
		# if len(comma) > 0:
		# 	stats['comma'] = 1
		# if len(period) > 0:
		# 	stats['period'] = 1
		# if len(qmark) > 0:
		# 	stats['questionmark'] = 1
		# if len(exmark) > 0:
		# 	stats['exclamationmark'] = 1

		###REAL VALUED FEATURES###
		if len(comma) > 0:
			stats['comma'] = len(comma)
		if len(period) > 0:
			stats['period'] = len(period)
		if len(qmark) > 0:
			stats['questionmark'] = len(qmark)
		if len(exmark) > 0:
			stats['exclamationmark'] = len(exmark)

		#attempt #2: fine annotation as further breakdown of task.

		for word in fine.split():
			#print(word, end="\t")
			wd = word.split(":")

			term = wd[0].lower()

			if term in labels:
				#retrieve mapped categories:
				mapped = labels[term]

				for m in mapped:
					###BINARY FEATURES##
					#stats[m] = 1

					###REAL VALUED###
					stats[m] += 1

			if len(wd) > 1:

				if wd[1]:
					annot = wd[1]
					annot = annot.replace("#", "").replace("*", "")

					for a in annot:
						#no real equivalent here for binary vs real-valued
						stats[a] = 1

		for s in stats:
			print(stats[s], end="\t")

		print()


trans_idx.close()







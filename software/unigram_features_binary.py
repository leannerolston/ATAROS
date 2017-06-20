#!/usr/bin/env
# -*- coding: utf-8 -*-

import os, sys

import nltk

dir = sys.argv[1]
printTask = sys.argv[2]

unigrams = []
COUNT = 10

files = [f for f in os.listdir(dir) if f.endswith("_cleaned.txt")]

#grab list of unigrams:
for f in files:
	with open(os.path.join(dir, f)) as inp:
		sentences = [l.strip() for l in inp]

		for line in sentences:

			tokens = line.split("\t")

			if len(tokens) < 2:
				continue
			elif len(tokens) < 3:
				text = line.split("\t")[1].replace("*", "")
			else:
				text = line.split("\t")[2].replace("*", "")

			unis = nltk.word_tokenize(text)

			truncs = [l for l, x in enumerate(unis) if len(x) > 1 and x.endswith("-")]
			abbrevs = [l for l, x in enumerate(unis) if len(x) > 1 and x.endswith("_")]

			if len(truncs) > 0:

				for t in truncs:
					unis[t] = "trunc"

			if len(abbrevs) > 0:
				for a in abbrevs:
					unis[a] = "abbrev"

			#Collapse duplicate words into one:
			if "mmmm" in unis:
				unis[unis.index("mmmm")] = "mm"

			#collapse mm-hmm into mm-hm
			if "mm-hm" in unis:
				unis[unis.index("mm-hm")] = "mm-hmm"

			if "mmhm" in unis:
				unis[unis.index("mmhm")] = "mm-hmm"

			if "mmkay" in unis:
				unis[unis.index("mmkay")] = "mm-kay"

			if "hm" in unis:
				unis[unis.index("hm")] = "hmm"

			if "aha" in unis:
				unis[unis.index("aha")] = "a-ha"

			unigrams.extend(unis)

unigrams = list(set(unigrams))
unigrams = sorted(unigrams)

#Do a count of features:
feature_count = [0] * len(unigrams)

for f in files:
	with open(os.path.join(dir, f)) as inp:
		sentences = [l.strip() for l in inp]

		for line in sentences:
			tokens = line.split("\t")

			if len(tokens) < 2:
				continue
			elif len(tokens) < 3:
				sentence = nltk.word_tokenize(tokens[1].replace("*", ""))
			else:
				sentence = nltk.word_tokenize(tokens[2].replace("*", ""))

			for s in sentence:

				if len(s) > 1 and s.endswith("-"):
					s = "trunc"

				if len(s) > 1 and s.endswith("_"):
					s = "abbrev"

				if s in unigrams:
					idx = unigrams.index(s)
					feature_count[idx] += 1

#find the features with count of more than COUNT

more_than_count = [l for l, x in enumerate(feature_count) if x >= COUNT]

valid_unigrams = []

for c in more_than_count:
	valid_unigrams.append(unigrams[c])

#Start printing:
print("speaker", end="\t")
if printTask == "Y":
	print("task", end="\t")
print("stance", end="\t")

for i in range(len(valid_unigrams)):
	if i < len(valid_unigrams) - 1:
		print(valid_unigrams[i], end="\t")
	else:
		print(valid_unigrams[i])


for f in files:
	with open(os.path.join(dir, f)) as inp:
		sentences = [l.strip() for l in inp]

		try:
			speaker = f[ : f.index("_cleaned.txt")]
		except ValueError:
			speaker = "Speaker"


		for line in sentences:
			tokens = line.split("\t")

			if len(tokens) < 2:
				continue

			stance = tokens[0]

			if len(tokens) < 3:
				sentence = nltk.word_tokenize(tokens[1].replace("*", ""))
				task = ""
			else:
				task = tokens[1]
				sentence = nltk.word_tokenize(tokens[2].replace("*", ""))

			features = [0] * len(valid_unigrams)

			print(speaker, end="\t")
			if task:
				print(task, end="\t")
			print(stance, end="\t")

			for s in sentence:

				if len(s) > 1 and s.endswith("-"):
					s = "trunc"

				if len(s) > 1 and s.endswith("_"):
					s = "abbrev"

				if s in valid_unigrams:
					idx = valid_unigrams.index(s)

					features[idx] = 1

			for i in range(len(features)):
				if i < len(features) - 1:
					print(features[i], end="\t")
				else:
					print(features[i])


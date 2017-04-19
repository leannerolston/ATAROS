#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, os, nltk

ataros_categories = sys.argv[1]
data_dir = sys.argv[2]

word_to_category_mapping = {}
#wcl[wd] = [cat, cat]
headings = [] #list of word categories


with open(ataros_categories) as inp:
	data = [l.strip() for l in inp if l]

for d in data:
	if not d:
		continue

	tokens = d.split("\t")

	cat = tokens[0]
	words = tokens[1].replace("*", "").split()

	for w in words:
		if w not in word_to_category_mapping:
			word_to_category_mapping[w] = []

		word_to_category_mapping[w].append(cat)

	headings.append(cat)

#print headings:
print("speaker\ttask\tstance", end="\t")

for i in range(len(headings)):
	if i < len(headings) - 1:
		print(headings[i], end="\t")
	else:
		print(headings[i])

files = [f for f in os.listdir(data_dir) if f.endswith(".txt") and f.startswith("NW")]

for f in files:
	with open(os.path.join(data_dir, f)) as inp:
		spurts = [l.strip() for l in inp if l]

		speaker = f[ : f.index("_cleaned.txt")]

		for s in spurts:

			tokens = s.split("\t")

			stance = tokens[0]
			task = tokens[1]

			text = tokens[2].replace("*", "").split()

			cats = []

			print(speaker, end="\t")
			print(task, end="\t")
			print(stance, end="\t")

			for t in text:
				if t in word_to_category_mapping:
					cats.extend(word_to_category_mapping[t])

			cats = list(set(cats))

			spurt_features = [0] * len(headings)


			for i in range(len(headings)):
				h = headings[i]

				if h in cats:
					spurt_features[i] = 1

			for i in range(len(spurt_features)):
				if i < len(spurt_features) - 1:
					print(spurt_features[i], end="\t")
				else:
					print(spurt_features[i])




















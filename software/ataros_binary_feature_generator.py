#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, os, nltk

ataros_categories = sys.argv[1]
data_dir = sys.argv[2]
printTask = sys.argv[3]

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

headings.append("longWds")
headings.append("totWds")

#print headings:
print("speaker", end="\t")
if printTask == "Y":
	print("task", end="\t")
print("stance", end="\t")

for i in range(len(headings)):
	if i < len(headings) - 1:
		print(headings[i], end="\t")
	else:
		print(headings[i])



files = [f for f in os.listdir(data_dir) if f.endswith("_cleaned.txt")]

for f in files:
	with open(os.path.join(data_dir, f)) as inp:
		spurts = [l.strip() for l in inp if l]

		try:
			speaker = f[ : f.index("_cleaned.txt")]
		except ValueError:
			speaker = "Speaker"

		for s in spurts:

			tokens = s.split("\t")

			if len(tokens) < 2:
				continue

			stance = tokens[0].replace("+", "").replace("-", "").replace("X", "").replace("x", "").replace("#", "").strip()


			if len(tokens) < 3:
				text = tokens[1].strip()
				task = ""
			else:
				task = tokens[1].strip()
				text = tokens[2].replace("*", "").split()


			cats = []

			print(speaker, end="\t")
			if task:
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
				elif h == "longWds":
					long = [l for l, x in enumerate(text) if len(x) >= 6]

					if len(long) > 1:
						spurt_features[i] = 1
				elif h == "totWds":
					spurt_features[i] = len(text)


			for i in range(len(spurt_features)):
				if i < len(spurt_features) - 1:
					print(spurt_features[i], end="\t")
				else:
					print(spurt_features[i])


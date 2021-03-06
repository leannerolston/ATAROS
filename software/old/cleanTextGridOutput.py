#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, nltk

from cleanText import cleanText

with open(sys.argv[1]) as inp:
	data = [l.strip() for l in inp]

for line in data:
	tokens = line.split("\t")

	if len(tokens) < 2:
		continue

	text = tokens[0].replace("*", "")
	stance = tokens[1].replace("+", "").replace("-", "").replace("X", "").replace("x", "").replace("#", "").strip()

	if len(tokens) > 2:
		task = tokens[2]
	else:
		task = ""

	if not stance:
		continue

	ct = cleanText(text)
	cleaned = ct.clean_text()

	if not cleaned:
		continue

	tokenized = nltk.word_tokenize(cleaned)
	cleaned = " ".join(tokenized)

	print(stance, end="\t")
	if task:
		print(task, end="\t")
	print(cleaned)





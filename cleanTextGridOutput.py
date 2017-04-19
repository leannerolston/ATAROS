#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys

from cleanText import cleanText

with open(sys.argv[1]) as inp:
	data = [l.strip() for l in inp]

for line in data:
	tokens = line.split("\t")

	if len(tokens) < 3:
		continue

	text = tokens[0]
	stance = tokens[1].replace("+", "").replace("-", "").replace("X", "").replace("x", "")
	task = tokens[2]

	if not stance:
		continue

	ct = cleanText(text)
	cleaned = ct.clean_text()

	if not cleaned:
		continue

	print(stance, end="\t")
	print(task, end="\t")
	print(cleaned)





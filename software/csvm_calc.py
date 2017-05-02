#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, regex

import operator

model_file = sys.argv[1]
headings_file = sys.argv[2]

with open(headings_file) as inp:
	data = inp.read()
	data = data.strip()

#Remove columns 0:2 since they're "speaker task stance"
headings = data.split("\t")[3:]

#Since we're using the index returned by e1071, add a blank cell at index[0]
headings.insert(0, "")

sv_header_pattern = regex.compile(r'^SV$')
label_pattern = regex.compile(r'^label ')

sums = [0] * len(headings)

with open(model_file) as inp:
	data = [l.strip() for l in inp]


#find out labels:
label_idx = [i for i, x in enumerate(data) if regex.match(label_pattern, x)]
labels = data[label_idx[0]].split()[1:]

sv_header_idx = [i for i, x in enumerate(data) if regex.match(sv_header_pattern, x)]

for sv in data[sv_header_idx[0] + 1: ]:
	feats = sv.split()

	vector_weights = []

	start_idx = 0

	for i in range(len(feats)):
		if not ":" in feats[i]:
			vector_weights.append(feats[i])
		else:
			start_idx = i
			break

	for cell in feats[start_idx:]:
		idx = int(cell.split(":")[0])
		value = float(cell.split(":")[1])

		for w in vector_weights:
			sums[idx] += float(w) * value

maximums = sorted(range(len(sums)), key=lambda k: abs(sums[k]), reverse = True)

#print(maximums)

for m in maximums:
	print(headings[m], end="\t")
	print(sums[m])






















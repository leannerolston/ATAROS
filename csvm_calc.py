#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, regex

import operator

model_file = sys.argv[1]

headings = ["", "period", "comma", "questionmark", "exclamationmark",
				"pronoun", "ipron", "ppron", "singPPron", "plurPPron", "1stPPron",
            "2ndPPron", "3rdPPron", "defArt", "indefArt", "function", "prep",
            "conj", "filler", "nonflu", "swear", "tentat", "differ",
            "discrep", "certain"]


sv_header_pattern = regex.compile(r'^SV$')
label_pattern = regex.compile(r'^label ')

sums = [0] * 25

with open(model_file) as inp:
	data = [l.strip() for l in inp]


#find out labels:
label_idx = [i for i, x in enumerate(data) if regex.match(label_pattern, x)]
labels = data[label_idx[0]].split()[1:]
print(labels)

sv_header_idx = [i for i, x in enumerate(data) if regex.match(sv_header_pattern, x)]

for sv in data[sv_header_idx[0] + 1: ]:
	feats = sv.split()
	#print(sv)

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

maximums = sorted(range(len(sums)), key=lambda k: sums[k], reverse = True)

#print(maximums)

for m in maximums:
	print(headings[m], end="\t")
	print(sums[m])






















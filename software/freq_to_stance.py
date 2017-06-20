#!/usr/bin/env
# -*- coding: utf-8 -*-

import os,sys

dir = sys.argv[1]

words = {}
#words[word][stance] = counts

files = [f for f in os.listdir(dir) if f.endswith(".txt")]

for f in files:
	with open(os.path.join(dir, f)) as inp:
		data = [l.strip("\n") for l in inp]

		for line in data:
			tokens = line.split("\t")

			stance = tokens[0]
			task = tokens[1]
			text = tokens[2].split()

			for wd in text:
				if wd not in words:
					words[wd] = {}

				if stance not in words[wd]:
					words[wd][stance] = 1
				else:
					words[wd][stance] += 1

tot_num = 0

counts = {}

for word in words:

	count = 0
	stances = []
	for stance in words[word]:
		count += words[word][stance]
		stances.append(stance)


	tot_num += count

	tup = count, stances
	counts[word] = tup

for word in counts:
	print(word, end="\t")

	count = counts[word][0]
	stances = counts[word][1]

	print(count/tot_num, end="\t")

	print(count, end="\t")

	print(stances)












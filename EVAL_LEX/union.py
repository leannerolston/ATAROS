#!/usr/bin/env
# -*- coding: utf-8 -*-

import os, sys

dir = sys.argv[1]
stance = sys.argv[2]

files = [f for f in os.listdir(dir)]


wds = set()

for f in files:
	with open(os.path.join(dir, f)) as inp:
		for line in inp:
			line = line.strip("\n")

			words = line.split("\t")[2]

			tokens = words.split()

			for t in tokens:
				wds.add(t)

with open(stance) as inp:
	for line in inp:

		line = line.strip("\n")
		if line in wds:
			print(line)


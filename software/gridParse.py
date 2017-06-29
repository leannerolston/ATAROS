#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, os, regex

dir = sys.argv[1]

tier_block = regex.compile(r'\s+item \[[0-9]+\]:')
interval_block = regex.compile(r'\s+intervals \[[0-9]+\]:')

def getFine(dial_act, w_start, w_end, f_idx):

	#go through dial act until we find the a span that approx matches our
	#transcription span

	for f in range(f_idx, len(dial_act)):
		f_start = float(dial_act[f][0])
		f_end = float(dial_act[f][1])
		fine = dial_act[f][2].strip()

		if f_end <= w_start:
			continue
		elif f_start >= w_end:
			return
		else:
			#print(f_start, f_end, fine)
			print(fine, end=" ")

		f_idx = f



def alignIntervals(grid, speaker, task):

	tier_heading_idx = [l for l, x in enumerate(grid) if regex.match(tier_block, x)]

	transcriptions = []
	stances = []
	dial_act = []
	words = []

	for i in range(len(tier_heading_idx)):
		tier_heading = grid[tier_heading_idx[i]]
		tier_name = grid[tier_heading_idx[i] + 2]

		tier_name = tier_name[tier_name.index("=") + 1:].replace("\"", "").strip()
		if tier_name == "phone":
			continue

		if i < len(tier_heading_idx) - 1:
			tier_range = grid[tier_heading_idx[i]:tier_heading_idx[i + 1]]
		else:
			tier_range = grid[tier_heading_idx[i]:]

		interval_idx = [l for l, x in enumerate(tier_range) if regex.match(interval_block, x)]

		for j in range(len(interval_idx)):
			interval = interval_idx[j]
			start_time = tier_range[interval + 1].strip()
			start_time = start_time[start_time.index("=") + 1:].strip()
			end_time = tier_range[interval + 2].strip()
			end_time = end_time[end_time.index("=") + 1:].strip()
			text = tier_range[interval + 3].strip()
			text = text[text.index("=") + 1:].replace("\"", "").strip()

			tup = start_time, end_time, text

			if tier_name == "word":
				words.append(tup)
			elif tier_name == "transcription":
				transcriptions.append(tup)
			elif tier_name == "coarse":
				stances.append(tup)
			elif tier_name == "fine":
				dial_act.append(tup)

	w_idx = 0
	f_idx = 0

	for t in range(len(transcriptions)):
		t_start = float(transcriptions[t][0])
		t_end = float(transcriptions[t][1])
		trans = transcriptions[t][2]

		if trans.strip() == "sp":
			continue

		print(speaker, end="\t")
		print(task, end="\t")

		#print("TRANS", t_start, t_end, trans)

		s_start = float(stances[t][0])
		s_end = float(stances[t][1])
		stance = stances[t][2]
		#print("STANCE", s_start, s_end, stance)

		print(stance, end="\t")
		print(trans, end="\t")
		#print("TRANS:", t_start, t_end)

		#Go into words, and wiz through the words whose end times are less than
		#the stance and transcription ending.
		for w in range(w_idx, len(words)):
			w_start = float(words[w][0])
			w_end = float(words[w][1])
			word = words[w][2].strip()

			if word == "sp":
				continue

			#print("WORD", w_start, w_end, word)

			#We need w_start > trans_start.  Otherwise, we need to bump word up
			if w_start >= t_start and w_end <= t_end:
				print(word, end=":")
				getFine(dial_act, w_start, w_end, f_idx)
			elif w_end < t_start:
				#w needs to catch up:
				#w_idx = w
				continue
			elif w_start > t_end:
				#w_idx = w
				break

			w_idx = w

		print()
		#print()



files = [l for l in os.listdir(dir)]

for f in files:
	try:
		with open(os.path.join(dir, f)) as inp:
			grid = [l.strip("\n") for l in inp.readlines()]
	except UnicodeDecodeError:
		with open(os.path.join(dir,f ), encoding='utf-16') as inp:
			grid = [l.strip("\n") for l in inp.readlines()]

	speaker1 = f[:f.index("-")]
	rest = f[f.index("-") + 1:]
	speaker2 = rest[:rest.index("-")]
	rest = rest[rest.index("-") + 1:]
	task = rest[:rest.index("-")]

	tier_heading_idx = [l for l, x in enumerate(grid) if regex.match(tier_block, x)]

	half_idx = int(len(tier_heading_idx)/2)
	first_speaker = tier_heading_idx[:half_idx]
	second_speaker = tier_heading_idx[half_idx:]

	#want to isolate grids for each speaker:
	first_speaker_grid = grid[first_speaker[0]:second_speaker[0]]
	second_speaker_grid = grid[second_speaker[0]:]

	alignIntervals(first_speaker_grid, speaker1, task)
	alignIntervals(second_speaker_grid, speaker2, task)




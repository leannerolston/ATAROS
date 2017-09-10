#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys, os

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

#SentiWordNet:
with open("SentiWordNet_3.0.0_20130122.txt") as inp:
	data = [l.strip() for l in inp if l]

SWN_Scores = {}
#SWN_scores[word] = pos,neg, pos

for line in data:
	if line.startswith("#"):
		continue

	tokens = line.split("\t")

	pos = tokens[0]
	POS = float(tokens[2])
	NEG = float(tokens[3])
	word = tokens[4]

	#Zero scores and scores under 0.2 removed:
	if not POS > 0.0 and not NEG > 0.0:
		continue

	words = [l[:l.index("#")] for l in word.split()]

	for word in words:
		tup = POS, NEG, pos
		SWN_Scores[word] = tup

with open("Ratings_Warriner_et_al.csv") as inp:
	data = [l.strip() for l in inp]

header = data[1]

NORMS_Scores = {}

#word - 1
#valence - 2
#arousal - mean - 5
#dominance - 8

for line in data[1:]:
	tokens = line.split(",")
	word = tokens[1]

	valence = float(tokens[2])
	arousal = float(tokens[5])
	dominance = float(tokens[8])

	#users asked to use 0 - 9 scale. 5 is neutral.
	#valence: unhappy - happy - distance from 5
	#arousal: calm - excited - distance over 5?
	#dominance: controlled - in control - distance from 5?

	if word not in NORMS_Scores:
		NORMS_Scores[word] = {}

		valence_score = abs(5 - valence)

		tup = valence_score, arousal, dominance
		NORMS_Scores[word] = tup

	else:
		print(word, arousal, dominance, valence)

#EvaluativeLexcon
with open("EvaluativeLexicon.txt") as inp:
	data = [l.strip() for l in inp]

EL_Scores = {}
#EL_Scores[word] = score
#Valence
#Extremety - derived from valence - 0-5
#Emotionality - 0-9

for line in data[1:]:
	tokens = line.split("\t")

	word = tokens[0].lower()
	extremity = float(tokens[2])
	emotionality = float(tokens[3])

	tup = extremity, emotionality
	EL_Scores[word] = tup


#NRC Affect Intensity Lexicon
with open("NRC-AffectIntensity-Lexicon.txt") as inp:
	data = [l.strip() for l in inp]

NRC_Scores = {}
#NRC_Scores[word] = score, dim
for line in data:
	tokens = line.split("\t")

	if len(tokens) < 3:
		continue

	word = tokens[0]

	if word in NRC_Scores:
		old_tup = NRC_Scores[word]
		old_score = old_tup[0]
	else:
		old_score = 0


	try:
		score = float(tokens[1])
	except ValueError:
		continue

	dim = tokens[2]

	if score > old_score:
		tup = score, dim
		NRC_Scores[word] = tup


#SUBJECTIVITY MARKERS

subjClues = {}
#sc[word] = type, pos, pol

with open("/Users/rolston/Desktop/ATAROS/MPQA/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff") as inp:
	for line in inp:
		tokens = line.split()

		type = tokens[0][ tokens[0].index("=") + 1 : ]
		word = tokens[2][ tokens[2].index("=") + 1 :]
		pos = tokens[3][ tokens[3].index("=") + 1 : ]

		pol = tokens[-1][ tokens[-1].index("=") + 1 : ]

		tup = type, pos, pol
		subjClues[word] = tup

#SOMASUDARAN ARGLEX:
#Intensifiers:
argLex = []
argLex_intensifiers = []

with open("/Users/rolston/Desktop/ATAROS/MPQA/arglex_Somasundaran07/intensifiers.tff") as inp:
	for line in inp:
		if line.startswith("@"):
			startidx = line.index("{")
			endidx = line.index("}")

			wds = line[startidx + 1: endidx].split(",")

			for wd in wds:
				if wd not in argLex:
					argLex.append(wd.strip())

				if wd not in argLex_intensifiers:
					argLex_intensifiers.append(wd.strip())

#Priority:
with open("/Users/rolston/Desktop/ATAROS/MPQA/arglex_Somasundaran07/priority.tff") as inp:
	for line in inp:
		if line.startswith("#"):
			continue

		line = line.strip()

		if line not in argLex:
			argLex.append(line)

#Necessity:
with open("/Users/rolston/Desktop/ATAROS/MPQA/arglex_Somasundaran07/necessity.tff") as inp:
	for line in inp:
		if line.startswith("#") or line.startswith("("):
			continue

		line = line.strip()

		if line not in argLex:
			argLex.append(line)

#Contrast
with open("/Users/rolston/Desktop/ATAROS/MPQA/arglex_Somasundaran07/contrast.tff") as inp:
	for line in inp:
		if line.startswith("#") or line.startswith("("):
			continue

		line = line.strip()

		if line not in argLex:
			argLex.append(line)


#Causation
with open("/Users/rolston/Desktop/ATAROS/MPQA/arglex_Somasundaran07/causation.tff") as inp:
	for line in inp:
		if line.startswith("#") or line.startswith("("):
			continue

		line = line.strip()

		if line not in argLex:
			argLex.append(line)


#OPINION LEX:
opLex_pos = []
opLex_neg = []
opLex = []

with open("/Users/rolston/Desktop/ATAROS/OpinionLex/positive-words.txt") as inp:
	for line in inp:
		line = line.strip()

		if not line or line.startswith(";"):
			continue

		if line not in opLex_pos:
			opLex_pos.append(line)

		if line not in opLex_neg:
			opLex_neg.append(line)

		if line not in opLex:
			opLex.append(line)

with open("/Users/rolston/Desktop/ATAROS/OpinionLex/negative-words.txt") as inp:
	for line in inp:
		line = line.strip()

		if not line or line.startswith(";"):
			continue

		if line not in opLex_neg:
			opLex_neg.append(line)

		if line not in opLex:
			opLex.append(line)


#EffectLexicon:
Effect_plus = []
Effect_minus = []
Effect = []

with open("/Users/rolston/Desktop/ATAROS/MPQA/effectwordnet/EffectWordNet.tff") as inp:
	for line in inp:
		line = line.strip()

		tokens = line.split("\t")

		sign = tokens[1]
		words = tokens[2].split(",")

		if sign == "Null":
			continue

		for word in words:
			if word not in Effect:
				Effect.append(word)

			if sign.startswith("+"):
				if word not in Effect_plus:
					Effect_plus.append(word)

			elif sign.startswith("-"):
				if word not in Effect_minus:
					Effect_minus.append(word)

with open("/Users/rolston/Desktop/ATAROS/MPQA/effectwordnet/goldStandard.tff") as inp:
	for line in inp:
		line = line.strip()

		tokens = line.split("\t")

		sign = tokens[1]
		words = tokens[2].split(",")

		#Revisit this:
		if sign == "Null":
			continue

		for word in words:
			if word not in Effect:
				Effect.append(word)

			if sign.startswith("+"):
				if word not in Effect_plus:
					Effect_plus.append(word)

			elif sign.startswith("-"):
				if word not in Effect_minus:
					Effect_minus.append(word)


#Open ATAROS NOW.
ataros_dir = sys.argv[1]

#Figure out headings:
#_sum - sum of all scored words in spurt.
#_num_wds - number of words in spurt receiving a score (TODO: Change to non-zero?)
#_max - score of the word in the spurt with the highest score
#_score_rate - # scored words / totWds
#_score_per_word - sum / totWds
#_mean_score - sum / num_wds
print("speaker\ttask\tstance", end="\t")
print("SWN_sum\tSWN_num_wds\tSWN_max\tSWN_score_rate\tSWN_score_per_word\tSWN_mean_score", end="\t")
#NORMS Valence:
print("NORMS_sum\tNORMS_num_wd\tNORMS_max\tNORMS_score_rate\tNORMS_score_per_word\tNORMS_mean_score", end="\t")
#NORMS arousal and dominance:
print("NORMS_ar_sum\tNORMS_ar_max\tNORMS_ar_score_per_word\tNORMS_ar_mean_score", end="\t")
print("NORMS_dom_sum\tNORMS_dom_max\tNORMS_dom_score_per_word\tNORMS_dom_mean_score", end="\t")

print("EvalLex_sum\tEvalLex_num_wd\tEvalLex_max\tEvalLex_score_rate\tEvalLex_score_per_word\tEvalLex_mean_score", end="\t")
print("EvalLex_emo_sum\tEvalLex_emo_max\tEvalLex_emo_score_per_word\tEvalLex_emo_mean_score", end="\t")

print("NRC_sum\tNRC_num_wds\tNRC_max\tNRC_score_rate\tNRC_score_per_word\tNRC_mean_score", end="\t")
#combined scores from all sets:
print("Emo_sum\tEMO_num_wds\tEMO_max\tEMO_score_rate\tEMO_score_per_word\tEMO_mean_score", end="\t")
#subjectivity markers:
print("SUBJ_totmarkers\tSUBJ_proportion", end="\t")
print("argLex\targLex_prop", end="\t")
print("opLex\topLex_prop", end="\t")
print("effectLex\teffectLex_prop", end="\t")
print("totalSubj\ttotalSubj_prop", end="\t")
print("totwds\ttext")

files = [f for f in os.listdir(ataros_dir) if f.endswith("_cleaned.txt")]

for f in files:
	with open(os.path.join(ataros_dir, f)) as inp:
		spurts = [l.strip() for l in inp if l]

		try:
			speaker = f[ : f.index("_cleaned.txt")]
		except ValueError:
			speaker = "Speaker"

		for s in spurts:
			tokens = s.split("\t")

			if len(tokens) < 2:
				continue

			stance = tokens[0].replace("+", "").replace("-", "").replace("X", "")
			stance = stance.replace("x", "").replace("#", "").replace("*", "").strip()

			if len(tokens) < 3:  #no task; fcic data
				text = tokens[1].split()
				task = "NULL"

			else:
				task = tokens[1].strip()
				text = tokens[2].replace("*", "").split()

			print(speaker, end="\t")
			print(task, end="\t")
			print(stance, end="\t")

			swn_sum = 0
			swn_tot_wds = 0
			swn_max = 0

			norms_sum = 0
			norms_tot_wds = 0
			norms_max = 0

			norms_arousal_sum = 0
			norms_arousal_max = 0
			norms_arousal_tot_wds = 0

			norms_dominance_sum = 0
			norms_dominance_max = 0
			norms_dominance_tot_wds = 0

			el_sum = 0
			el_tot_wds = 0
			el_max = 0

			el_emo_sum = 0
			el_emo_max = 0
			el_emo_tot_wds = 0

			nrc_sum = 0
			nrc_tot_wds = 0
			nrc_max = 0

			#Combined Strength:
			#SWN and NRC are from 0 - 1.  NORMS is 0 - 9
			#Normalize NORMS to be between 0 and 9 by dividing value by 9:
			#Union of all scores:
			combined_sum = 0
			combined_tot_wds = 0
			combined_max = 0

			tot_wds = 0

			#SUBJECTIVE
			markers = 0
			strong_markers = 0
			weak_markers = 0

			al_markers = 0

			op_lex = 0

			ef_lex = 0

			combined_subj = 0

			for t in text:

				tot_wds += 1

				#used to calculate emotiobal union
				swn_tmp = 0
				norms_tmp = 0
				nrc_tmp = 0
				el_tmp = 0
				denom = 0
				word_union = 0

				lem = lemmatizer.lemmatize(t)

				#SentiWordNet:
				if lem in SWN_Scores:
					term = lem
				elif t in SWN_Scores:
					term = t
				else:
					term = ""

				if term:
					sc = SWN_Scores[term]
					pos = sc[0]
					neg = sc[1]

					swn_sum += max(pos, neg)

					if max(pos, neg) > 0.2:
						swn_tot_wds += 1

					swn_tmp = max(pos,neg)

					if swn_tmp > swn_max:
						swn_max = swn_tmp

				#NORMS:
				if t in NORMS_Scores:
					term = t
				elif lem in NORMS_Scores:
					term = lem
				else:
					term = ""

				if term:
					tuple = NORMS_Scores[term]

					valence = tuple[0]
					arousal = tuple[1]
					dominance = tuple[2]

					if valence > 1:
						norms_tot_wds += 1

					norms_sum += valence

					norms_tmp = valence

					if valence > norms_max:
						norms_max = valence

					norms_arousal_sum += arousal
					norms_arousal_tot_wds += 1

					if arousal > norms_arousal_max:
						norms_arousal_max = arousal

					norms_dominance_sum += dominance
					norms_dominance_tot_wds += 1

					if dominance > norms_dominance_max:
						norms_dominance_max = dominance

				#EvalLex:
				if lem in EL_Scores:
					term = lem
				elif t in EL_Scores:
					term = t
				else:
					term = ""

				if term:

					tup = EL_Scores[term]

					extremity = tup[0]
					emotionality = tup[1]

					if extremity > 1:
						el_tot_wds += 1

					el_sum += extremity
					el_tmp = extremity

					if el_tmp > el_max:
						el_max = el_tmp

					el_emo_sum += emotionality
					el_emo_tot_wds += 1

					if emotionality > el_emo_max:
						el_emo_max = emotionality

				#NRC:
				if lem in NRC_Scores:
					term = lem
				elif t in NRC_Scores:
					term = t
				else:
					term = ""

				if term:
					tup = NRC_Scores[term]

					score = tup[0]

					if score > 0.2:
						nrc_tot_wds += 1

					nrc_sum += score

					if score > nrc_max:
						nrc_max = score

					nrc_tmp = score

				#Union of emotional scores:
				word_union_numerator = swn_tmp + nrc_tmp + norms_tmp/5 + el_tmp/5

				denom = 0
				if swn_tmp > 0:
					denom += 1
				if nrc_tmp > 0:
					denom += 1
				if norms_tmp > 0:
					denom += 1
				if el_tmp > 0:
					denom += 1

				if denom > 0:
					word_union = word_union_numerator/denom
				else:
					word_union = 0

				if word_union > 0:
					combined_tot_wds += 1

				combined_sum += word_union

				if word_union > combined_max:
					combined_max = word_union

				#SubjClues:
				if t in subjClues:
					term = t
				elif lem in subjClues:
					term = lem
				else:
					term = ""

				if term:
					markers += 1

					tup = subjClues[term]
					type = tup[0]
					pos = tup[1]

					# if type == "strongsubj":
					# 	strong_markers += 1

					# elif type == "weaksubj":
					# 	weak_markers += 1

				#ARGLEX:
				if t in argLex:
					term = t
				elif lem in argLex:
					term = lem
				else:
					term = ""

				if term:
					al_markers += 1

					# if term in argLex_intensifiers:
					# 	al_intensifiers += 1

				#OpLex:
				if t in opLex:
					term = t
				elif lem in opLex:
					term = lem
				else:
					term = ""

				if term:
					op_lex += 1

					# if term in opLex_pos:
					# 	op_lex_pos += 1

					# if term in opLex_neg:
					# 	op_lex_neg += 1

				if t in Effect:
					term = t
				elif lem in Effect:
					term = lem
				else:
					term = ""

				if term:
					ef_lex += 1

					# if term in Effect_plus:
					# 	ef_lex_plus += 1

					# if term in Effect_minus:
					# 	ef_lex_neg += 1


				#COMBINED SUBJ Clues:
				if t in subjClues or lem in subjClues or t in opLex or lem in opLex \
					or t in argLex or lem in argLex or t in Effect or lem in Effect:
					combined_subj += 1

			print(swn_sum, end="\t")
			print(swn_tot_wds, end="\t")
			print(swn_max, end="\t")
			print(swn_tot_wds/tot_wds, end="\t")
			print(swn_sum/tot_wds, end="\t")
			if swn_tot_wds > 0:
				print(swn_sum/swn_tot_wds, end="\t")
			else:
				print(0, end="\t")

			#NORMS:
			print(norms_sum, end="\t")
			print(norms_tot_wds, end="\t")
			print(norms_max, end="\t")
			print(norms_tot_wds/tot_wds, end="\t")
			print(norms_sum/tot_wds, end="\t")
			if norms_tot_wds > 0:
				print(norms_sum/norms_tot_wds, end="\t")
			else:
				print(0, end="\t")

			print(norms_arousal_sum, end="\t")
			print(norms_arousal_max, end="\t")
			print(norms_arousal_sum/tot_wds, end="\t")
			if norms_arousal_tot_wds > 0:
				print(norms_arousal_sum/norms_arousal_tot_wds, end="\t")
			else:
				print(0, end="\t")

			print(norms_dominance_sum, end="\t")
			print(norms_dominance_max, end="\t")
			print(norms_dominance_sum/tot_wds, end="\t")
			if norms_dominance_tot_wds > 0:
				print(norms_dominance_sum/norms_dominance_tot_wds, end="\t")
			else:
				print(0, end="\t")

			print(el_sum, end="\t")
			print(el_tot_wds, end="\t")
			print(el_max, end="\t")
			print(el_tot_wds/tot_wds, end="\t")
			print(el_sum/tot_wds, end="\t")
			if el_tot_wds > 0:
				print(el_sum/el_tot_wds, end="\t")
			else:
				print(0, end="\t")

			print(el_emo_sum, end="\t")
			print(el_emo_max, end="\t")
			print(el_emo_sum/tot_wds, end="\t")
			if el_emo_tot_wds > 0:
				print(el_emo_sum/el_emo_tot_wds, end="\t")
			else:
				print(0, end="\t")

			print(nrc_sum, end="\t")
			print(nrc_tot_wds, end="\t")
			print(nrc_max, end="\t")
			print(nrc_tot_wds/tot_wds, end="\t")
			print(nrc_sum/tot_wds, end="\t")
			if nrc_tot_wds > 0:
				print(nrc_sum/nrc_tot_wds, end="\t")
			else:
				print(0, end="\t")

			#Union of Emotional Scores:
			print(combined_sum, end="\t")
			print(combined_tot_wds, end="\t")
			print(combined_max, end="\t")
			print(combined_tot_wds/tot_wds, end="\t")
			print(combined_sum/tot_wds, end="\t")
			if combined_tot_wds > 0:
				print(combined_sum/combined_tot_wds, end="\t")
			else:
				print(0, end="\t")

			#SUBJECTIVITY MARKERS:)
			print(markers, end="\t")
			print(markers/tot_wds, end="\t")

			print(al_markers, end="\t")
			print(al_markers/tot_wds, end="\t")


			print(op_lex, end="\t")
			print(op_lex/tot_wds, end="\t")

			print(ef_lex, end="\t")
			print(ef_lex/tot_wds, end="\t")

			print(combined_subj, end="\t")
			print(combined_subj/tot_wds, end="\t")

			print(tot_wds, end="\t")

			print(' '.join(text))

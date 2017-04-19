import regex





repeat = regex.compile(r'\(.*?x\)|[0-9]{1}x')
qual = regex.compile(r'\{.*?\}|\{.*?\)|\{.*?\]')
pause = regex.compile(r'\.\.')
unknown = regex.compile(r'\(\?\?\)')
paren = regex.compile(r'\(|\)')
stance_in_text = regex.compile(r'\.*[0-9]{1}x')
truncated = regex.compile(r'[a-zA-Z]+\- ')
breakoff = regex.compile(r' \-(?=$)')


allowed_contractions = ["\'m", "\'s", "\'re", "\'ll", "\'d", "\'ve"]


class cleanText:

	import regex

	def __init__(self, text):
		self.text = text

	def clean_text(self):

		text = self.text

		qualities = regex.findall(qual, text)

		for q in qualities:
			text = text.replace(q, "")

		repetitions = regex.findall(repeat, text)

		for r in repetitions:
			text = text.replace(r, "")

		pauses = regex.findall(pause, text)

		for p in pauses:
			text = text.replace(p, "")

		unknowns = regex.findall(unknown, text)

		for u in unknowns:
			text = text.replace(u, "")

		parens = regex.findall(paren, text)

		for p in parens:
			text = text.replace(p, "")

		stances_in_text = regex.findall(stance_in_text, text)

		for s in stances_in_text:
			text = text.replace(s, "")

		truncates = regex.findall(truncated, text)

		for t in truncates:
			text = text.replace(t, " TRUNC ")

		# breaks = regex.findall(breakoff, text)

		# for b in breaks:
		# 	text = text.replace(b, "")

		text = text.replace("*", " * ")
		text = text.replace("`", "")

		txt = text.split()

		txt = [l.lower() for l in txt]

		for i in range(len(txt)):
			if txt[i][0] == "\'" and txt[i] not in allowed_contractions:
				txt[i] = txt[i][1:]

		text = ' '.join(txt)

		return text




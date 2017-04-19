#Open files:
gridPath$ = "/Users/rolston/Desktop/ATAROS/textgrids/new/"
outputPath$ = "/Users/rolston/Desktop/ATAROS/"

clearinfo

Create Strings as file list: "grids", gridPath$ + "*.TextGrid"

gridLength = Get number of strings

for g from 1 to gridLength
	selectObject: "Strings grids"
	gridName$ = Get string: g

	#open textGrid:
	fullPath$ = gridPath$ + gridName$
	if fileReadable(fullPath$)
		Read from file... 'fullPath$'

	grid = selected("TextGrid")

	#Get task name:
	idx = index(gridName$, "_")
	rest$ = left$(gridName$, idx - 1)
	task$ = right$(rest$, 2)


	#Get info from speaker1: 
	intervals_ch1 = Get number of intervals: 1
	interval_name$ = Get tier name: 1
	#appendInfoLine: gridName$
	#appendInfo: interval_name$

	#check that number of intervals match:
	#intervals_ch2 = Get number of intervals: 2
	#if intervals_ch1 != intervals_ch2
	#	appendInfoLine: gridName$
	#endif

	if interval_name$ = "transcription" 
		idx = index(gridName$, "-")
		file_name$ = left$(gridName$, idx - 1)
	else
		file_name$ = interval_name$
	endif 

	#appendInfoLine: gridName$, " ", interval_name$, " ", file_name$
	for i from 1 to intervals_ch1
		speech$ = Get label of interval: 1, i
		stance$ = Get label of interval: 2, i
		#appendInfoLine: "speech: " + speech$
		#appendInfoLine: "stance: " + stance$ 
		#appendInfoLine: "task: " + task$
		
		appendFileLine: file_name$ + ".txt", speech$, tab$, stance$, tab$, task$
	endfor

		
	#Get info from speaker 2: 
	intervals_ch3 = Get number of intervals: 3
	interval_name$ = Get tier name: 3

	#check that number of intervals matches:
	#intervals_ch4 = Get number of intervals: 4
	#if intervals_ch3 != intervals_ch4
	#	appendInfoLine: gridName$
	#endif

	if interval_name$ = "transcription"
		idx = index(gridName$, "-")
		len = length(gridName$)
		rest$ = right$(gridName$, len - idx)
		idx = index(rest$, "-")
		file_name$ = left$(rest$, idx - 1)
	elsif index(interval_name$, "-") > 0
		dash_idx = index(interval_name$, "-")
		file_name$ = left$(interval_name$, dash_idx - 1)
	else
		file_name$ = interval_name$	
	endif 

	#appendInfoLine: gridName$, " ", interval_name$, " ", file_name$

	for i from 1 to intervals_ch3
		speech$ = Get label of interval: 3, i
		stance$ = Get label of interval: 4, i
		#appendInfoLine: "speech: " + speech$
		#appendInfoLine: "stance: " + stance$ 
		#appendInfoLine: "task: " + task$
		appendFileLine: file_name$ + ".txt", speech$, tab$, stance$, tab$, task$

	endfor


endfor



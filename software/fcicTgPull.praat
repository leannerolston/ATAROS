#Open files:
gridPath$ = "/Users/rolston/Desktop/ATAROS/FCIC/"
outputPath$ = "/Users/rolston/Desktop/ATAROS/tg_out"

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

	#Get trancription tier: 
	intervals_trans = Get number of intervals: 3

	#Get coarse tier:
	intervals_coarse = Get number of intervals: 4

	#check that number of intervals match:
	#if intervals_trans != intervals_coarse
	#	appendInfoLine: gridName$
	#endif

	#Get name of file:
	idx = index(gridName$, "-aligned")
	file_name$ = left$(gridName$, idx - 1)

	idx = rindex(file_name$, "-")
	idx = length(file_name$) - idx
	file_name$ = right$(file_name$, idx)

	for i from 1 to intervals_trans
		speech$ = Get label of interval: 3, i
		stance$ = Get label of interval: 4, i
		appendInfoLine: "speech: " + speech$
		appendInfoLine: "stance: " + stance$ 
		
		appendFileLine: file_name$ + ".txt", speech$, tab$, stance$	
	endfor

endfor



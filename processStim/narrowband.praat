#	Create narrow band filtered sounds ('telephone/radio effect') from a directory
# of recordings.
#
# Change sourceDirectory$ & outputDirectory$ to preferred directories (make sure
# these exist), change minFreq & maxFreq to edit the pass band (narrower =
# stronger effect).
#
#	Marianne de Heer Kloots, 7-6-2016

sourceDirectory$ = "/Users/mariannedhk/testsounds/"
outputDirectory$ = "/Users/mariannedhk/testsounds/filtered/"
minFreq = 300
maxFreq = 3000

strings = Create Strings as file list: "fileList", sourceDirectory$ + "/*.wav"
numberOfFiles = Get number of strings

for iFile to numberOfFiles
  selectObject: strings
	fileName$ = Get string: iFile
	rawSound = Read from file: sourceDirectory$ + fileName$
  selectObject: rawSound
  filteredSound = Filter (pass Hann band): minFreq, maxFreq, 100
  Save as WAV file: outputDirectory$ + fileName$
  removeObject: rawSound, filteredSound
endfor

removeObject: strings

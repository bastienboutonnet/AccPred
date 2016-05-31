#	Get some time data from TextGrid
#
#	J J A Pacilly, 18-may-2013, for Bastien Boutonnet

form Scale Peak or Intensity
  sentence FileSpec   *.TextGrid
  sentence ResultFile Data.txt
  endform

deleteFile: resultFile$
appendFileLine: resultFile$, "fileName	totalLen	onsetDet	onsetNoun	offsetNoun"

idStr   = Create Strings as file list: "fileList", fileSpec$
nrFiles = Get number of strings

for file to nrFiles
  selectObject: idStr
  fn$     = Get string: file

  idTG    = Read from file: fn$
  oname$  = selected$("TextGrid")
  nrTiers = Get number of tiers
  nrInt   = Get number of intervals: 1
  assert nrTiers == 1
  assert nrInt   == 4

  ts      = Get start time
  te      = Get end time
  totDur  = Get total duration
  t2 = Get starting point: 1, 2
  t3 = Get starting point: 1, 3
  t4 = Get starting point: 1, 4

  appendFileLine: resultFile$, oname$, tab$, fixed$(totDur, 3), tab$, fixed$(t2, 3), tab$, fixed$(t3, 3), tab$, fixed$(t4, 3)
  removeObject: idTG
  endfor

removeObject: idStr

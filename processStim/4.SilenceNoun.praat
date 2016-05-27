#	Silence noun
#
#	J J A Pacilly, 18-may-2013, for Bastien Boutonnet

form Scale Peak or Intensity
  sentence FileSpec   *.TextGrid
  #sentence ResultFile Data.txt # MAYBE THIS NEEDS TO CHANGE.
  endform

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

  t1 = Get starting point: 1, 3

  t2 = Get end point: 1, 3

  idSf = Read from file: oname$ + ".wav"

  Set part to zero: t1, t2, "at nearest zero crossing"
  Save as WAV file: oname$ + "_silenced.wav"
  removeObject: idTG, idSf
  endfor

removeObject: idStr

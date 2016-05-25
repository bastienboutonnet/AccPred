#	Concatenate part one of fileA to part two of fileB on the
#	the base of a text-file. Optionally intensity normalised.
#
#	J J A Pacilly, 18-may-2016, for Bastien Boutonnet

form Splice
  comment Normalise the intensity level for each part
  boolean  Normalise no
  positive Intensity_(dB) 70
  endform


idStr = Read Table from tab-separated file: "splicePattern.txt"

nrRows = Get number of rows
nrCols = Get number of columns

for row to nrRows
  selectObject: idStr
  fNameA$ = Get value: row, "fileA"
  fNameB$ = Get value: row, "fileB"
  fNameR$ = Get value: row, "fileR"

  idTGa = Read from file: fNameA$ + ".TextGrid"
  nrTiers = Get number of tiers
  assert nrTiers == 1
  nrInt = Get number of intervals: 1
  assert nrInt == 4
  t1 = Get starting point: 1, 1
  t2 = Get starting point: 1, 2
  idTGpA = Extract part: t1, t2, "no"

  idSndA  = Read from file: fNameA$ + ".wav"
  idPartA = Extract part: t1, t2, "rectangular", 1, "no"
  if normalise
    Scale intensity: intensity
    endif

  idTGb = Read from file: fNameB$ + ".TextGrid"
  nrTiers = Get number of tiers
  assert nrTiers == 1
  nrInt = Get number of intervals: 1
  assert nrInt == 4
  t3 = Get starting point: 1, 2
  t4 = Get end point: 1, 4
  idTGpB = Extract part: t3, t4, "no"

  idSndB  = Read from file: fNameB$ + ".wav"
  idPartB = Extract part: t3, t4, "rectangular", 1, "no"
  if normalise
    Scale intensity: intensity
    endif

  selectObject: idTGpA, idTGpB
  idTGResult = Concatenate
  Save as text file: "./spliced/" + fNameR$ + ".TextGrid"

  selectObject: idPartA, idPartB
  idResult = Concatenate
  if not normalise
    Save as WAV file: "./spliced/" + fNameR$ + ".0.wav"
  else
    Save as WAV file: "./spliced/" + fNameR$ + ".1.wav"
    endif
  removeObject: idTGa, idTGpA, idSndA, idPartA, idTGb, idTGpB, idSndB, idPartB, idTGResult, idResult
  endfor


removeObject: idStr

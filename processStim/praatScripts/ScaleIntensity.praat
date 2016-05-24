#	Scale Intensity of selected files in a directory
#
#	J J A Pacilly, 22-feb-2013, for Yiya Chen
#	J J A Pacilly, 29-mar-2016, made ByGroup feature optional, for Yiya Chen

form Scale Peak or Intensity
  sentence Directory P:/My Documents/Work/Yiya/ScaleIntensity/
  sentence FileSpec *.wav
  sentence ResultDir Scaled/
  comment Select ByGroup to preserve the relative intensity difference between files
  comment To set the intensity level for each individual file, do NOT select ByGroup
  boolean  ByGroup no
  optionmenu Scale_Method 2
    option Peak
    option Intensity
  positive Peak_(value)    0.99
  positive Intensity_(dB) 70
  endform

idStr   = Create Strings as file list: "fileList", directory$ + fileSpec$
nrFiles = Get number of strings

if nrFiles == 0
  removeObject: idStr
  exit "No files found"
  endif

for file to nrFiles
  selectObject: idStr
  fn$[file] = Get string: file
  idI[file] = Read from file: directory$ + fn$[file]
  endfor
removeObject: idStr

selectObject: idI[1]
for file from 2 to nrFiles
  plusObject: idI[file]
  endfor

if byGroup
  Concatenate recoverably
  idChainSnd = selected("Sound")
  idChainTG  = selected("TextGrid")
  selectObject: idChainSnd
  endif

if scale_Method$ == "Peak"
  Scale peak: peak
elif scale_Method$ == "Intensity"
  Scale intensity: intensity
  endif

if not byGroup
  for file to nrFiles
    selectObject: idI[file]
    Save as WAV file: directory$ + resultDir$ + fn$[file]
    removeObject: idI[file]
    endfor
else
  selectObject: idChainTG
  nrIntervals = Get number of intervals: 1
  assert nrFiles == nrIntervals

  selectObject: idChainSnd, idChainTG
  Extract all intervals: 1, "no"
  nrObjects = numberOfSelected("Sound")
  assert nrFiles == nrObjects

  for file to nrObjects
    idO[file] = selected("Sound", file)
    endfor

  for file to nrObjects
    selectObject: idO[file]
    Save as WAV file: directory$ + "/" + resultDir$ + fn$[file]
    removeObject:  idI[file], idO[file]
    endfor
  removeObject: idChainSnd, idChainTG
  endif

1:
	echo "Step 1: renaming files"
	python 1.renameFiles.py

2:
	echo "Step 2: generating file list"
	python 2.listFilesAndCodeConds.py

3:
	echo "Step 3: assign splicings Pick *Filename* File"
	python 3.assignSplicing.py

4:
	echo "Step 4: generate splice pattern. Pick *spliceAssigned* File"
	python 4.genSplicePattern.py

5:
	echo "Copying Praat Splice Script to processing hub"
	cp 3.Splice.praat ../stimToProcess/3.Splice.praat
	mkdir ../stimToProcess/spliced/

6:
	echo "Renaming Spliced Files"
	mv ../stimToProcess/spliced/ ./spliced/
	python 5.renameSplicedFiles.py

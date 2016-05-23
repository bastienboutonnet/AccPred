## Renames filenames
## To run directly from the current directory

import os, re

path=os.getcwd()
filenames=os.listdir(path)

for filename in filenames:
    # firstPattern, up to _part
    firstSubs=re.sub(r"\_[ab]\_(Bobby|Jurriaan|Johanneke|Victoria)",'',filename)
    # second Sub to remobe '_part'
    newName=re.sub(r"\_part",'',firstSubs)

    os.rename(filename,newName)

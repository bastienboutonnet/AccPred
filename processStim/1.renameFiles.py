## Renames filenames
## To run directly from the current directory

import os, re

def renameForProcessing(path):
    os.chdir(path)
    filenames=os.listdir(path)
    #remove from experimental sentences
    for filename in filenames:
        # firstPattern, up to _part
        firstSubs=re.sub(r"\_[ab]\_(Bobby|Jurriaan|Johanneke|Victoria)",'',filename)
        #os.rename(filename,firstSubs)
        # second Sub to remobe '_part'
        newName=re.sub(r"\_part",'',firstSubs)
        os.rename(filename,newName)

    #remove from control sentences
    filenames=os.listdir(path) #gotta somehow refresh filenames
    for filename in filenames:
        # firstPattern, up to _part
        controlSubs=re.sub(r"\_(Bobby|Jurriaan|Johanneke|Victoria)",'',filename)
        os.rename(filename,controlSubs)

if __name__=='__main__':
    renameForProcessing(path='../stimToProcess/')

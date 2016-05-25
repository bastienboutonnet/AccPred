## Renames filenames
## To run directly from the current directory

import os, re

def renameAfterSplice(path):
    filenames=os.listdir(path)
    os.chdir(path)
    #remove from experimental sentences
    for filename in filenames:
        # firstPattern, up to _part
        if filename.endswith('.TextGrid'):
            newName=re.sub(r"\_spliced",'',filename)
        else:
            newName=re.sub(r"\_spliced.[01]",'',filename)
        os.rename(filename,newName)

if __name__=='__main__':
    renameAfterSplice(path='./spliced/')

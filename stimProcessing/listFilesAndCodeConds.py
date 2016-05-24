import os, re
import pandas as pd

def listNames(path,addSpliceOptions=False):
    filenames=os.listdir(path)
    count = 0
    for filename in filenames:
        if filename.endswith(".wav"):
            curSentID=re.findall(r'\d+',filename)
            curRel=re.findall(r'(\_related|\_unrelated|\_control)',filename)
            curRel=re.sub(r"\_",'',curRel[0])
            #isControl=re.findall(r'control',filename)
            #if curRel!=['related'] and isControl!=['control']:
                #curRel='unrelated'
           # else:
                #curRel='control'
            if count<1:
                fileList=pd.DataFrame({'filename':filename,'sentID':curSentID,'rel':curRel})
            else:
                curFileRow=pd.DataFrame({'filename':filename,'sentID':curSentID,'rel':curRel})
                fileList=fileList.append(curFileRow)
            count += 1
    fileList=fileList.reset_index(drop=True)
    if addSpliceOptions==True:
        fileList['keepCont']=""
        fileList['splice']=""
    return fileList

if __name__=='__main__':
    import time
    t=time.strftime("%m%d%H%M")
    filesDf=listNames(path='../stimToProcess/',addSpliceOptions=True)
    filesDf.to_csv('filenames'+t+'.csv', index=False)

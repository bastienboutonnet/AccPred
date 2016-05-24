import os, re
import pandas as pd

def listNames(path):
    filenames=os.listdir(path)
    count = 0
    for filename in filenames:
        if filename.endswith(".wav"):
            curSentID=re.findall(r'\d+',filename)
            curRel=re.findall(r'related',filename)
            if curRel!=['related']:
                curRel='unrelated'
            if count<1:
                fileList=pd.DataFrame({'filename':filename,'sentID':curSentID,'rel':curRel})
            else:
                curFileRow=pd.DataFrame({'filename':filename,'sentID':curSentID,'rel':curRel})
                fileList=fileList.append(curFileRow)
            count += 1
    fileList=fileList.reset_index(drop=True)
    return fileList

if __name__=='__main__':
    path=''
    filesDf=listNames(path)
    filesDf.to_csv('filenames.csv')

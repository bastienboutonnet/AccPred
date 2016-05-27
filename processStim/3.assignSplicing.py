import pandas as pd
import numpy as np

def assignSplicingRules(df):
    split=np.array_split(df,2)
    for curDf in xrange(len(split)):
        if curDf==0:
            split[curDf].loc[split[curDf].rel=='related',['keepCont','splice']]=1,0
            split[curDf].loc[split[curDf].rel=='unrelated',['keepCont','splice']]=0,1
        else:
            split[curDf].loc[split[curDf].rel=='related',['keepCont','splice']]=0,1
            split[curDf].loc[split[curDf].rel=='unrelated',['keepCont','splice']]=1,0


    concated=pd.concat(split)
    return concated

if __name__=='__main__':
    import easygui
    import time
    t=time.strftime("%m%d%H%M")
    filename=easygui.fileopenbox(filetypes=['*.csv'])
    df=pd.read_csv(filename)
    spliceAssignments=assignSplicingRules(df)
    spliceAssignments.to_csv('spliceAssigned'+t+'.csv',index=False)

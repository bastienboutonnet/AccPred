import pandas as pd
import numpy as np
import os
from numpy.random import RandomState
from itertools import product

######## FUNCTIONS
#----------------------
def simple_shuffle(frame, block=None, times=10, seed=None, resetInd=False):
    prng = RandomState(seed)

    def _shuffle(chunk):
        for _ in range(times):
            chunk = chunk.reindex(prng.permutation(chunk.index))
        if resetInd is True:
            chunk=chunk.reset_index(drop=True)
        return chunk

    if block is None:
        return _shuffle(frame)
    else:
        return frame.groupby(block).apply(_shuffle)

def add_blocks(frame, size, name='block', condList=None, id_col=None, start_at=0):

    def _assigner(lim,size):
        num = 0
        n=0
        while n<=lim:
            if n % size == 0 and n != 0:
                num +=1
                n += 1
                #print blocks[num],n, num
                yield blocks[num]
            else:
                n +=1
                #print blocks[num],n,num
                yield blocks[num]

    if condList is None:
        blocks=range(len(frame)/size)
    else:
        blocks=condList

    assigner=_assigner(len(frame),size)

    def _add(chunk):
        chunk[name]=[assigner.next() for _ in xrange(len(chunk))]
        return chunk

    if id_col is None:
        new_frame=_add(frame).sort_values(by=name)
    else:
        new_frame=frame.groupby(id_col).apply(_add).sort_values(by=id_col)

    if condList is None:
        #new_frame[name]=new_frame[name]+start_at
        return new_frame
    else:
        new_frame[name]=new_frame[name]
        return new_frame

def addTrig(df):
    if df['speaker']=='Nat' and df['relatedness']=='related':
        return '11'
    if df['speaker']=='Nat' and df['relatedness']=='unrelated':
        return '12'
    if df['speaker']=='nonNat' and df['relatedness']=='related':
        return '21'
    if df['speaker']=='nonNat' and df['relatedness']=='unrelated':
        return '22'

## Lexical Descision trials



def main(subjCode,whichTask,seed=None):
    ######IMPLEMENT A SHUFFLE HERE
    dbase=pd.read_csv('./database/120allAbove70.csv',encoding='utf-16')
    df=pd.DataFrame({'sentID':dbase['sentID']})
    df=simple_shuffle(df,seed=seed).reset_index(drop=True)
    rel=add_blocks(df,60,name='relatedness',condList=['related','unrelated'])
    speak=add_blocks(df,30,name='speaker',condList=['Nat','nonNat','Nat','nonNat'])
    speak=speak[['speaker','sentID','relatedness']]
    speak['filename']=speak.apply(lambda x: '_'.join(x.dropna().astype(str).values),axis=1)
    speak=speak.sort_values(by="relatedness")
    final=simple_shuffle(speak,seed=seed).reset_index(drop=True)

    #Merge Experiment needed info from Database
    dBaseToMerge=dbase[['sentID','hasQuestion','Question','yesOrNo','compLower','unrelOppositeGender']]
    hasQmerge=pd.merge(final,dBaseToMerge,how='left',on='sentID')
    hasQmerge['part']='experiment'

    #Merge Timings
    timings=pd.read_table('./database/timings.txt',sep='\t')
    hasTimings=pd.merge(hasQmerge,timings,how='left',on='filename')
    hasTimings=hasTimings[hasTimings.sentID != 130]

    #Add Controls
    # controls=pd.read_csv('../database/controlSentences.csv')
    # controls['trigDet']=55
    # controls['trigOffsetNoun']=155
    # subControls=controls.sample(n=60,replace=False,random_state=seed)
    controls=pd.read_table('./database/expControls.txt',encoding='utf-16')
    controls=controls[['speaker','sentID','relatedness','filename','hasQuestion','Question','yesOrNo','part','totalLen','onsetDet','onsetNoun','offsetNoun','waitForDetOffset','waitForNounOffset','waitForEnd','newWord1','newWord2']]
    controls['trigDet']=55
    controls['trigOffsetNoun']=155

    #Add Triggers
    hasTimings['trigDet']=hasTimings.apply(lambda row: addTrig(row),axis=1)
    hasTimings['trigOffsetNoun']=hasTimings.trigDet+"9"

    #Join Experimental trials and controls
    trialsAndControls=pd.concat([hasTimings,controls]).reset_index(drop=True)

    #Shuffle For Good measure!
    finalTrials=simple_shuffle(trialsAndControls,seed=seed).reset_index(drop=True)

    #Add Trial index
    finalTrials['trialIndex']=xrange(1,len(finalTrials)+1)

    #Process practice trials
    practSents=pd.read_csv('./database/practiceSentences.csv',encoding='utf-16',sep='\t')
    practSents['trialIndex']=0
    practSents['trigDet']=0
    practSents['trigOffsetNoun']=0
    ##########

    ##Lexical Descision Lists
    expTr=finalTrials.copy()
    expTr['isOld']=1
    expTr['trialIndex']=0

    cntNew=pd.read_table('./database/lexOnlyControls.txt',encoding='utf-16')
    lexTrials=pd.concat([expTr,cntNew]).reset_index(drop=True)
    lexTrials=simple_shuffle(lexTrials,seed=seed).reset_index(drop=True)
    lexTrials['trialIndex']=xrange(1,len(lexTrials)+1)


    #finalTrials=hasTimings ##I Think this step will drop since I wanna separate files.

    #finalTrials['trigDet']=finalTrials.apply(lambda row: addTrig(row),axis=1)
    #finalTrials['trigOffsetNoun']=finalTrials.trigDet+"9"




###################################### ADD FAKE TRIAL HERE
    #testPres=pd.Series(finalTrials.filename.append(pd.Series({'filename':['fuck']})))


    #RUN A FILE CHECK, to make sure each file is in
    missing=pd.Series()
    filenames=os.listdir('./stimuli/')
    for curSent in finalTrials.filename:

        if str(curSent)+".wav" not in filenames:
            missing=missing.append(pd.Series([curSent]))
            print curSent
    if not missing.empty:
        missing.to_csv('missingFiles'+subjCode+'.csv',index=False)
        print 'Looks like there were some missing files. Check log'
        raise SystemExit
    #only save file if the files aren't missing -hence the break
    if whichTask=='accPred':
        practSents.to_csv('trials/trialListPract_' +subjCode +'.csv',encoding='utf-8',index=False)
        finalTrials.to_csv('trials/trialList_' +subjCode +'.csv',encoding='utf-8',index=False)
    if whichTask=='lexRecall':
    #lexTrials.to_csv('trials/trialListLex_'+subjCode+'.csv',encoding='utf-16',index=False)
        lexTrials.to_excel('trials/trialListLex_'+subjCode+'.xlsx',encoding='utf-16',index=False)
    return (finalTrials, practSents,lexTrials,missing)


if __name__ == "__main__":
    import time
    #t=time.strftime("%m%d%H%M")
    #(finalTrials,practSents,lexTrials,missing)=main('dummySubject'+t,seed=1)
    (finalTrials,practSents,lexTrials,missing)=main('dummySubject',whichTask="accPred",seed=1)

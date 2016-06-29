import pandas as pd
import numpy as np
import os
from numpy.random import RandomState
from itertools import product
from labtools.trials_functions import *
from labtools.generator_functions import *


def addTrig(df):
    if df['speaker']=='Nat' and df['relatedness']=='related':
        return '11'
    if df['speaker']=='Nat' and df['relatedness']=='unrelated':
        return '12'
    if df['speaker']=='nonNat' and df['relatedness']=='related':
        return '21'
    if df['speaker']=='nonNat' and df['relatedness']=='unrelated':
        return '22'
#Item Definition
# items = ['congRight','congLeft','incongRight','incongLeft']
# cong= ['cong','cong','incong','incong']
# direction=['Right','Left']
# items = pd.DataFrame({'item':items,'cong':cong,}, index = pd.Index(range(len(items)),
#                                                       name = 'item_id'))
#
# flank = pd.DataFrame({'flanker':items['item'].values})
# flank = extend(flank, reps = 4, rep_ix = 'flanker_iter',
#                 row_ix = 'flanker_id')
#
# #Generate But not
# nonMatches=generate_but_not(stroop, items, on = ['letters','item'],
#                  source_cols = {'item':'color'}, seed = 124)
# nonMatches['congr']=0
# nonMatches['trig']=11
#
# #Generate Matches
# matches=generate_matches(stroop, items, on = ['letters','item'],
#                  source_cols = {'item':'color'}, seed = 124)
# matches['congr']=1
# matches['trig']=22
#
# #Stick Together
# allTrials=pd.concat([nonMatches,matches]).reset_index(drop=True)
#
# #Shuffle No Repeat
# shuffled=smart_shuffle(allTrials,col='letters_id',seed=124)
#
# flank = pd.DataFrame({'direction':['left','right'],'dirCode':[1,2]})
# flank = expand(flank, 'congruent', values=[1,2], ratio=0.5)
# flank['trigCode']=flank[['congruent','dirCode']].apply(lambda x: ''.join(x.values.astype(str)),axis=1)
# flankTrials=extend(flank,reps=20) # Change Number To get Enough Trials
#
# #Shuffle No Repeat
# shuffled=smart_shuffle(flankTrials,col='trigCode',seed=124)

def main(subjCode,howMany=20,seed=None):
    ######IMPLEMENT A SHUFFLE HERE
    flank = pd.DataFrame({'direction':['left','right'],'dirCode':[0,1]})
    flank = expand(flank, 'congruent', values=[1,2], ratio=0.5)
    flank['trigCode']=flank[['congruent','dirCode']].apply(lambda x: ''.join(x.values.astype(str)),axis=1)
    flankTrials=extend(flank,reps=howMany) # Change Number To get Enough Trials

    #Shuffle No Repeat
    shuffled=smart_shuffle(flankTrials,col='trigCode',seed=seed)

    #Add TrialIndex
    shuffled['trialIndex']=xrange(1,len(shuffled)+1)
    shuffled['part']='experiment'
    shuffled.to_csv('trials/trialList_Flanker_' +subjCode +'.csv',encoding='utf-8',index=False)

    return (flank,shuffled)


if __name__ == "__main__":
    import time
    t=time.strftime("%m%d%H%M")
    #(finalTrials,practSents,lexTrials,missing)=main('dummySubject'+t,seed=1)
    shuffled=main('dummySubject'+t,seed=1)

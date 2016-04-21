import random
import itertools
import numpy
import pandas as pd

list=['s1,.6,2.4','s2,.6,1.8','s3,3,4.2']
separator=','

def	main(subjCode,seed,numTrials):
    seed = int(seed)
    random.seed(int(seed))
    testFile = open('trials/trialList_'+subjCode+ '.csv','w')
    trialList=[]
    #header
    print >>testFile, separator.join(("soundFile", "stdTrig", "devTrigg"))
    prevTrialContent= curTrialContent = False
    for curBlock in range(numTrials):
        curTrialContent=random.choice(list)
        while prevTrialContent==curTrialContent:
            curTrialContent=random.choice(list)
        prevTrialContent=curTrialContent

        trialList.append(str(curTrialContent))

    for curTrialList in trialList:
        print >>testFile, curTrialList

if __name__ == "__main__":
    trialList = main('testTrials-13',13,50)

import pandas as pd
import numpy as np
import itertools

def generateCircular(frame, source, col_name):
    circular=itertools.cycle(source)
    g_frame=pd.concat([pd.Series({col_name:circular.next()}) for _ in xrange(len(frame))],axis=1).T
    frame[col_name]=g_frame[col_name]
    return frame

def generateByGroup(frame, source, col_name, by):

    def _generate_for_group(grp):
        circ=itertools.cycle(source)
        g_frame=pd.concat([pd.Series({col_name:circ.next()}) for _ in xrange(len(grp))],axis=1).T
        g_frame.index=grp.index
        return g_frame

    grouped_frame=frame.groupby(by, group_keys=False).apply(_generate_for_group)
    grouped_frame=frame[col_name]=grouped_frame[col_name]
    return frame #Or use return grouped_frame for only the output of the column, since in any case the original frame gets transformed.



itemList=pd.DataFrame({'items':list(range(1,11))})
list=['pred','nonpred']
itemList['lang']=np.where(itemList['items']<=5,'eng','nl')

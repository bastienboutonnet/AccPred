import pandas as pd
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

def genTr(frame,firstBlockSize, secondBlockSize, firstBlockName, secondBlockName,seedOfShuffle=None):
    #df=simple_shuffle(df)
    rel=add_blocks(frame,firstBlockSize,name=firstBlockName,condList=['related','unrelated'])
    speak=add_blocks(rel,secondBlockSize,name=secondBlockName,condList=['native','nonNative','native','nonNative'])
    speak.sort_values(by=firstBlockName)

    return speak

###IMPLEMENTATION
###-----------------------
if __name__ == "__main__":
    

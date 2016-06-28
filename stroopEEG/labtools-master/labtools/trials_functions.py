#!/usr/bin/env python
"""
labtools.trials_functions
"""
import pandas as pd

from numpy.random import RandomState
from itertools import product

def counterbalance(conditions, order=None):
    """
    Generate all independent variable combinations in a DataFrame.
    
    Each row of the resulting DataFrame contains a unique combination of 
    conditions. Use primarily for full counterbalancing of within-subject 
    variables.
    
    :param dict conditions: Variable names and possible values. Values can be
        of length 1.
    :param order: Optional order of columns in output.
    :type order: list or None
    :return: Each row is a unique combination of input variables, assuming the 
        possible values for each variable are unique.
    :rtype: pandas.DataFrame
    """
    for k,v in conditions.items():
        if not hasattr(v, '__iter__'):
            conditions[k] = [v]
    
    combinations = list(product(*conditions.values()))
    frame = pd.DataFrame(combinations, columns=conditions.keys())
    
    if order is None:
        order = frame.columns
    
    return frame[order]
    
def expand(valid, name, values=[1,0], ratio=0.5, sample=False, seed=None):
    """
    Copy rows as necessary to satisfy the valid:invalid ratio.
        
    Use when complete counterbalancing is not plausible. For example, when the 
    ratio of trials requiring response A to those requiring response B is not
    50:50.
    
    :param pandas.DataFrame valid: Trial list to be expanded.
    :param str name: Name of new column containing valid and invalid values
    :param list values: Values for valid and invalid trials, respectively.
    :param float ratio: Desired percentage of valid trials in the resulting 
        frame. Must be between 0 and 1. Defaults to 0.5.
    :param bool sample: Should the invalid trials be sampled from the valid 
        trials? If True, len(returned) < 2*len(valid). Defaults to False.
    :param seed: Seed random number generator.
    :type seed: int or None
    :return: New trial list with valid and invalid trials are denoted in a 
        new column.
    :rtype: pandas.DataFrame
    """
    prng = RandomState(seed)
    num_trials = len(valid)
    
    if not sample:
        invalid = valid[:]
        num_valid = (num_trials*ratio)/(1.0-ratio)
        copies = int(num_valid/num_trials)
        valid = pd.concat([valid]*copies, ignore_index=True)
    else:
        num_invalid = int((num_trials*(1.0-ratio))/ratio)
        sampled = prng.choice(valid.index, num_invalid, replace=False)
        invalid = valid.reindex(sampled).reset_index(drop=True)
    
    frame = pd.concat([valid, invalid], keys=values, names=[name,'DEFAULT'])
    frame = frame.reset_index().drop('DEFAULT', axis=1)
    return frame
    
def extend(frame, reps=None, max_length=None, rep_ix=None, row_ix=None):
    """
    Duplicates the unique trials for a total length less than the provided max.
    
    Either `reps` or `max_length` must be specified. If both are provided, reps
    takes priority.
    
    :param pandas.DataFrame frame: Trials to be extended.
    :param reps: Number of times to copy the frame.
    :type reps: int or None
    :param max_length: Specify a max number of trials.
    :type max_length: int or None
    :param rep_ix: Column name for the iteration of repetitions.
    :type rep_ix: str or None
    :param row_ix: Column name for the row identification, which
                   is the original index of frame.
    :type row_ix: str or None
    :returns: Duplicated trials
    :rtype: pandas.DataFrame
    """
    if not hasattr(reps, '__iter__'):
        reps = reps or max_length/len(frame)
        if reps < 1:
            reps = 1
        reps = range(reps)
    
    col_names = [rep_ix or 'DEFAULT1', row_ix or 'DEFAULT2']
    
    to_drop = ['DEFAULT1', 'DEFAULT2']
    if rep_ix is not None:
        to_drop.remove('DEFAULT1')
    if row_ix is not None:
        to_drop.remove('DEFAULT2')
    
    repeated = pd.concat([frame]*len(reps), keys=reps, names=col_names).reset_index()
    return repeated.drop(to_drop, axis=1)

def add_block(frame, size, name='block', start_at=0, id_col=None, seed=None):
    """
    Creates a new column for block.
    
    :param pandas.DataFrame frame: Trials to be assigned blocks.
    :param int size: Length of each block.
    :param id_col: Column to group by before blocking. Assures that blocks 
        consist of approximately the same number of trials for each unique
        value in id_col
    :type id_col: str or None
    :param seed: Seed random number generator.
    :type seed: int or None
    :returns: Trial list with new column for block.
    :rtype: pandas.DataFrame
    """
    def _assigner(blocks, prng):
        prng.shuffle(blocks)
        i = 0
        while True:
            yield blocks[i]
            if (i+1)%len(blocks):
                prng.shuffle(blocks)
            i = (i+1)%len(blocks)
            
    prng = RandomState(seed)
    blocks = range(len(frame)/size)
    assigner = _assigner(blocks, prng)
    
    def _add(chunk):
        chunk[name] = [assigner.next() for _ in xrange(len(chunk))]
        return chunk
    
    if id_col is None:
        new_frame = _add(frame).sort(name)
    else:
        new_frame = frame.groupby(id_col).apply(_add).sort(name)
    
    new_frame[name] = new_frame[name] + start_at
    return new_frame
                
def simple_shuffle(frame, block=None, times=10, seed=None):
    """
    Shuffles trials a few times.
    
    :param pandas.DataFrame frame: Trials to be shuffled.
    :param block: Optional column to groupby before shuffling.
    :type block: str or None.
    :param int times: Number of times to shuffle. Defaults to 10.
    :param seed: Seed random number generator.
    :type seed: int or None
    :returns: Trial list with rows in random order.
    :rtype: pandas.DataFrame
    """
    prng = RandomState(seed)
    
    def _shuffle(chunk):
        for _ in range(times):
            chunk = chunk.reindex(prng.permutation(chunk.index))
        return chunk
    
    if block is None:
        return _shuffle(frame)
    else:
        return frame.groupby(block).apply(_shuffle)

def smart_shuffle(frame, col, block=None, seed=None, verbose=False, lim=10000):
    """
    Shuffles trials such that equivalent trials never appear back to back.
    
    :param pandas.DataFrame frame: Trials to be shuffled.
    :param str col: Column of values to minimize repetitions.
    :param block: Column to groupby before shuffling.
    :type block: str or None
    :param seed: Seed random number generator.
    :type seed: int or None
    :param bool verbose: Should the status of randomization be printed? Defaults
        to False.
    :param int lim: Maximum number of shuffles before giving up. Defaults to
        10000.
    :returns: Trial list with rows in randomized order.
    :rtype: pandas.DataFrame
    """
    prng = RandomState(seed)
        
    def _shuffle(chunk):
        orig_index = chunk.index
        repeats = None
        for i in xrange(lim):
            new = chunk.reindex(prng.permutation(chunk.index))
            r = (new[col][1:]==new[col][:-1]).sum()
            if repeats is None or r < repeats:
                repeats = r
                chunk = new
            if repeats == 0:
                break
        if i==lim-1 and verbose:
            print 'Iteration limit reached! Minimum repeats: ', str(repeats)
        
        chunk.index = orig_index
        return chunk
    
    if block is None:
        return _shuffle(frame)
    else:
        return frame.groupby(block).apply(_shuffle)

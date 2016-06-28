#!/usr/env/bin python
import pandas as pd
import numpy as np

from trials_functions import expand, extend, add_block

class TrialsMaker(object):
    def __init__(self, seed=None, trials=None):
        self.seed = seed
        self.trials = trials
    
    def set_trials(self, df):
        """
        Set the base trials for the trials maker.
        
        :param df: pandas.DataFrame.
        """
        self.trials = df[:]
    
    def expand(ratio, name, values=[1,0], sample=False):
        """
        Copy rows as necessary to satisfy the valid:invalid ratio.
        """
        self.trials = expand(self.trials, name, values, ratio, 
                             sample, self.seed)
    
    def extend(reps=None, max_length=None, rep_ix=None, row_ix=None):
        """
        Duplicate the unique trials for a total length less than the max.
        """
        self.trials = extend(self.trials, reps, max_length, rep_ix, row_ix)
    
    def add_block(size, name='block', start_at=0, id_col=None):
        """
        Create a new column for block.
        """
        self.trials = add_block(self.trials, size, name, start_at, id_col, seed)

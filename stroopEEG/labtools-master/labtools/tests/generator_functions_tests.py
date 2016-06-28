#! /usr/bin/env python
import unittest

import pandas as pd
from numpy import *

import string

from ..trials_functions import counterbalance, expand
from ..generator_functions import generate, generate_by_group, generate_but_not

class TestGenerate(unittest.TestCase):
    def setUp(self):
        _vars = {'a':random.choice(arange(100), 10, replace=False), 
                 'b':random.choice(list(string.letters), 10, replace=False),
                 'c':[0,1]}
        
        self.trials = counterbalance(_vars)
        self.info = counterbalance({'x':_vars['b'],'ix':range(5)})
    
    def test_single_col(self):
        col = 'x'
        self.trials = generate(self.trials, self.info, source_cols=col)
        matches = (self.trials[col].head(len(self.info)).values == \
                   self.info[col].values)
        self.assertTrue(matches.sum() == len(self.info))
    
    def test_multi_col(self):
        cols = ['x','ix']
        self.trials = generate(self.trials, self.info, 
                               source_cols=cols)
        for col in cols:
            matches = (self.trials[col].head(len(self.info)).values == \
                       self.info[col].values)
            self.assertTrue(matches.sum() == len(self.info))

class TestGenerateByGroup(unittest.TestCase):
    def setUp(self):
        _vars = {'a':random.choice(arange(100), 10, replace=False), 
                 'b':random.choice(list(string.letters), 10, replace=False),
                 'c':[0,1]}
        
        self.trials = counterbalance(_vars)
        sep = random.choice(list(string.letters), 10, replace=False)
        self.info0 = counterbalance({'x':sep[:5],'ix':range(1,5)})
        self.info1 = counterbalance({'x':sep[5:],'ix':range(5,10)})
    
    def test_group_by(self):
        source_map = {0: self.info0,
                      1: self.info1}
        self.trials = generate_by_group(self.trials, 'c', source_map)
        
        trials0 = self.trials['x'][self.trials['c'] == 0]        
        trials1 = self.trials['x'][self.trials['c'] == 1]
        
        for x in trials0.unique():
            self.assertTrue(x not in trials1)
        
        for y in trials1.unique():
            self.assertTrue(y not in trials0)

class TestGenerateButNot(unittest.TestCase):
    def setUp(self):
        _vars = {'a':random.choice(arange(100), 10, replace=False), 
                 'b':random.choice(list(string.letters), 10, replace=False),
                 'c':[0,1]}
        
        self.trials = counterbalance(_vars)
        self.info = counterbalance({'b':_vars['b'],'ix':range(5)})
    
    def test_but_not(self):
        self.trials = generate_but_not(self.trials, self.info, 
                                       on='b', source_cols={'b':'xb'})
        matches = (self.trials['xb'] == self.trials['b'])
        self.assertTrue(matches.sum() == 0)
    
    def test_but_not_separate(self):
        self.info = self.info.rename(columns={'b':'bb'})
        
        self.trials = generate_but_not(self.trials, self.info,
                                             on=['b','bb'], source_cols={'bb':'xb'})
        matches = (self.trials['xb'] == self.trials['b'])
        self.assertTrue(matches.sum() == 0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
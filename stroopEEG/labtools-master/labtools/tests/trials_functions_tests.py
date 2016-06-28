#! /usr/bin/env python
import unittest

import pandas as pd
import numpy as np

import string

from ..trials_functions import counterbalance, expand, extend

class CounterbalanceTests(unittest.TestCase):
    def test_unique(self):
        _vars = {'a':np.random.choice(np.arange(100), 10, replace=False), 
                 'b':np.random.choice(list(string.letters), 10, replace=False)}
        counter = counterbalance(_vars)
        counter['unique'] = counter['a'].astype(str) + counter['b']
        self.assertEqual(len(counter['unique'].unique()), len(counter))
    
    def test_types(self):
        _vars = {'a':np.random.choice(np.arange(100), 10, replace=False), 
                 'b':np.random.choice(list(string.letters), 10, replace=False),
                 'c':1,
                 'd':'test',
                 'e':-1.21}
        self.assertTrue(isinstance(counterbalance(_vars), pd.DataFrame))
    
    def test_order(self):
        _vars = {'a':np.random.choice(np.arange(100), 10, replace=False), 
                 'b':np.random.choice(list(string.letters), 10, replace=False),
                 'c':np.random.choice(list(string.letters), 10, replace=False)}
        var_order = _vars.keys()
        np.random.shuffle(var_order)
        counter = counterbalance(_vars, order=var_order)
        self.assertSequenceEqual(var_order, list(counter.columns))

class ExpandTests(unittest.TestCase):
    def test_sample(self):
        pass
    
    def test_copy(self):
        pass
    
    def test_seed(self):
        pass

class ExtendTests(unittest.TestCase):
    def setUp(self):
        _vars = {'a':np.random.choice(np.arange(100), 10, replace=False), 
                 'b':np.random.choice(list(string.letters), 10, replace=False)}
        self.trials = counterbalance(_vars)
    
    def test_extend(self):
        ext = extend(self.trials, reps=4)
        self.assertEquals(len(ext), len(self.trials)*4)
    
    def test_rep_over_max(self):
        ext = extend(self.trials, max_length=90, reps=4)
        self.assertEquals(len(ext), len(self.trials)*4)
    
    def test_max_length(self):
        test_max = 390
        ext = extend(self.trials, max_length=test_max)
        self.assertTrue(len(ext) < test_max)
    
    def test_dropped_col1(self):
        ext = extend(self.trials, reps=4, rep_ix='iter')
        self.assertTrue(('iter' in ext.columns and \
                         len(ext.columns) == len(self.trials.columns)+1))
    
    def test_dropped_col2(self):
        ext = extend(self.trials, reps=4, row_ix='id')
        self.assertTrue(('id' in ext.columns and \
                         len(ext.columns) == len(self.trials.columns)+1))

def main():
    unittest.main()

if __name__ == '__main__':
    main()

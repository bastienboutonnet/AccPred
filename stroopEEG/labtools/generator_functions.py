#!/usr/bin/env python
"""
labtools.generator_functions
"""
import pandas as pd

from numpy import arange
from numpy.random import RandomState

def _circular_generator(source, prng=None):
    """
    Yield rows from source with optional randomization.
    
    :param pandas.DataFrame source: Frame to yield from.
    :param prng: Optional randomizer.
    :type prng: numpy.random.RandomState or None
    :return: Yields rows from source.
    :rtype: pandas.Series
    """
    ix_options = source.index.tolist()
    num_options = len(ix_options)
    
    if prng is not None:
        prng.shuffle(ix_options)
    
    ix = 0
    while True:
        next_ix = ix_options[ix]
        yield source.ix[next_ix]
        ix = (ix+1)%num_options
        
        if prng is not None and ix%num_options == 0:
            prng.shuffle(ix_options)

def generate(frame, source, source_cols=None, seed=None):
    """
    Adds columns to a trial list from a source using a circular generator.
    
    :param pandas.DataFrame frame: Trial list.
    :param pandas.DataFrame source: Source list.
    :param source_cols: Columns of `source` to add to `frame`. Defaults to
        adding all columns of `source`. If `source_cols` is a dict, keys will be 
        renamed to values.
    :type source_cols: str, list, dict, or None
    :param seed: Seed random number generator.
    :type seed: int or None
    :return: The `frame` with additional `source_cols` from `source`.
    :rtype: pandas.DataFrame
    """
    prng = None
    
    if seed is not None:
        prng = RandomState(seed)
    
    if source_cols is None:
        source_cols = source.columns
    elif not hasattr(source_cols, '__iter__'):
        source_cols = [source_cols,]
    
    if not isinstance(source_cols, dict):
        source_cols = dict(zip(source_cols, source_cols))
    
    gen = _circular_generator(source, prng)
    g_frame = pd.concat([gen.next() for _ in xrange(len(frame))], axis=1).T
    g_frame = g_frame.convert_objects(convert_numeric = True)
    g_frame = g_frame[source_cols.keys()].rename(columns = source_cols)
    
    g_frame.index = frame.index
    frame[source_cols.values()] = g_frame[source_cols.values()]
    
    return frame

def generate_by_group(frame, by, source_map, source_cols=None, seed=None):
    """
    Adds columns to a trial list from multiple sources.
    
    Splits a trial list into chunks to add columns from various sources. Chunks
    are paired with sources based on unique values in `frame[by]`. See 
    :func:`generate` for more details.
    
    :param pandas.DataFrame frame: Trial list.
    :param str by: Grouping column in `frame`. Unique values are used as keys to
        get sources from `source_map`.
    :param dict source_map: Container of source lists. Keys are unique values of
        `frame[by]`. Values are pandas.DataFrame sources.
    :param source_cols: Columns of `source` to add to `frame`. Defaults to
        adding all columns of `source`. If `source_cols` is a dict, keys will be 
        renamed to values.
    :type source_cols: str, list, dict, or None
    :param seed: Seed random number generator. If `None` the result will not be
        randomized.
    :type seed: int or None
    :return: The `frame` with additional `source_cols` from `source`.
    :rtype: pandas.DataFrame
    """
    # create unique seeds for each part
    num_seeds = len(frame[by].unique()) + 1
    if seed is not None:
        prng = RandomState(seed)
        seeds = list(prng.choice(arange(1000), num_seeds))
    else:
        seeds = [None]*num_seeds
        
    def _generate_for_group(grp):
        group_key = grp[by].unique()[0]
        group_source = source_map[group_key]
        group_frame = generate(grp, group_source, source_cols, seeds.pop())
        group_frame.index = grp.index
        return group_frame
    
    return frame.groupby(by, group_keys=False).apply(_generate_for_group)

def create_source_map(source, on, source_keys, comparison_func):
    """
    Splits a source into groups using a comparison function.
    
    :param pandas.DataFrame source: Source list.
    :param str on: `source[on]` is used as an operand in `comparison_func`.
    :param list source_keys: Secondary operand in `comparison_func`.
    :param function comparison_func: Function to compare `source[on]` to 
        `source_keys`. Must return a boolean mask the same length as `source`.
    :return: Map of source_keys to subsets of the source that satisfy the 
        `comparison_func`
    :rtype: dict
    """
    source_map = {}
    for key in source_keys:
        select = comparison_func(source[on], key)
        source_map[key] = source[select]
    
    return source_map

def generate_matches(frame, source, on, source_cols=None, seed=None):
    """
    Adds columns to a trial list based on *matching* values in source.
    
    For more information:
        * on how the columns are added, see :func:`generate_by_group`.
        * on how the matching values are selected, see 
          :func:`create_source_map`
    
    :param pandas.DataFrame frame:
    :param pandas.DataFrame source: Full options to split into the source_map.
    :param on: Column names to match source and frame on.
    :type on: str or list
    :param source_cols: Columns of `source` to add to `frame`. Defaults to
        adding all columns of `source`. If `source_cols` is a dict, keys will be 
        renamed to values.
    :type source_cols: str, list, dict, or None
    :param seed: Seed random number generator. If `None` the result will not be
        randomized.
    :type seed: int or None
    :return: The `frame` with additional `source_cols` from sources.
    :rtype: pandas.DataFrame
    """
    if not isinstance(on, list):
        on = [on, on]
    f_on, s_on = on
    
    source_keys = frame[f_on].unique()
    
    def _is_equal(x, y): 
        return x == y
    
    source_map = create_source_map(source, s_on, source_keys, _is_equal)
    
    return generate_by_group(frame, f_on, source_map, source_cols, seed)

def generate_but_not(frame, source, on, source_cols=None, seed=None):
    """
    Adds columns to a trial list based on *non-matching* values in source.
    
    For more information:
        * on how the columns are added, see :func:`generate_by_group`.
        * on how the non-matching values are selected, see 
          :func:`create_source_map`
    
    :param pandas.DataFrame frame:
    :param pandas.DataFrame source: Full options to split into the source_map.
    :param on: Column names to match source and frame on.
    :type on: str or list
    :param source_cols: Columns of `source` to add to `frame`. Defaults to
        adding all columns of `source`. If `source_cols` is a dict, keys will be 
        renamed to values.
    :type source_cols: str, list, dict, or None
    :param seed: Seed random number generator. If `None` the result will not be
        randomized.
    :type seed: int or None
    :return: The `frame` with additional `source_cols` from sources.
    :rtype: pandas.DataFrame
    """
    if not isinstance(on, list):
        on = [on, on]
    f_on, s_on = on
    
    source_keys = frame[f_on].unique()
    
    def _is_not_equal(x, y):
        return x != y
    
    source_map = create_source_map(source, s_on, source_keys, _is_not_equal)
    
    return generate_by_group(frame, f_on, source_map, source_cols, seed)

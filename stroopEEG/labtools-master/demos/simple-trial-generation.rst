
Simple Trial Generation
=======================

This demo walks through some basics of trial generation using labtools
and pandas.

.. code:: python

    # this demo is located in the demos folder of the labtools project, available on GitHub
    import sys, os
    sys.path.insert(0, os.path.abspath('..'))
    
    import pandas as pd
    import numpy as np
    
    from labtools.trials_functions import *

.. parsed-literal::

    /Users/edmiston/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/pandas/io/excel.py:626: UserWarning: Installed openpyxl is not supported at this time. Use >=1.6.1 and <2.0.0.
      .format(openpyxl_compat.start_ver, openpyxl_compat.stop_ver))


counterbalance
--------------

One of the basic functions of trial generation is to allow for full
counterbalancing. The function ``counterbalance`` takes a ``dict`` of
variables and produces a ``pandas.DataFrame`` output.

                .. autofunction:: labtools.trials_functions.counterbalance
    :noindex:
                
.. code:: python

    my_variables = {'version':['a','b','c'], 'response':[1,2], 'session':2}
    counterbalance(my_variables, order=['version','session','response'])



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>version</th>
          <th>session</th>
          <th>response</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td> a</td>
          <td> 2</td>
          <td> 1</td>
        </tr>
        <tr>
          <th>1</th>
          <td> a</td>
          <td> 2</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>2</th>
          <td> b</td>
          <td> 2</td>
          <td> 1</td>
        </tr>
        <tr>
          <th>3</th>
          <td> b</td>
          <td> 2</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>4</th>
          <td> c</td>
          <td> 2</td>
          <td> 1</td>
        </tr>
        <tr>
          <th>5</th>
          <td> c</td>
          <td> 2</td>
          <td> 2</td>
        </tr>
      </tbody>
    </table>
    </div>



expand
------

                .. autofunction:: labtools.trials_functions.expand
    :noindex:
                
.. code:: python

    posner = pd.DataFrame({'target_dir':['left','right']})
    posner = expand(posner, 'valid_prime', ratio=0.75)
    posner



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>valid_prime</th>
          <th>target_dir</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>3</th>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>4</th>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>5</th>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>6</th>
          <td> 0</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>7</th>
          <td> 0</td>
          <td> right</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    posner = expand(posner, 'prime_type', values=['present', 'neutral'], ratio=0.5)
    posner['valid_prime'][posner['prime_type'] == 'neutral'] = -1
    posner



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>prime_type</th>
          <th>valid_prime</th>
          <th>target_dir</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0 </th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>1 </th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>2 </th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>3 </th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>4 </th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>5 </th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>6 </th>
          <td> present</td>
          <td> 0</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>7 </th>
          <td> present</td>
          <td> 0</td>
          <td> right</td>
        </tr>
        <tr>
          <th>8 </th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>9 </th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>10</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>11</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>12</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>13</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>14</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>15</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
      </tbody>
    </table>
    </div>



extend
------

                .. autofunction::labtools.trials_functions.extend
    :noindex:
                
.. code:: python

    extend(posner, reps = 2)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>prime_type</th>
          <th>valid_prime</th>
          <th>target_dir</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0 </th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>1 </th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>2 </th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>3 </th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>4 </th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>5 </th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>6 </th>
          <td> present</td>
          <td> 0</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>7 </th>
          <td> present</td>
          <td> 0</td>
          <td> right</td>
        </tr>
        <tr>
          <th>8 </th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>9 </th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>10</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>11</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>12</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>13</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>14</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>15</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>16</th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>17</th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>18</th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>19</th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>20</th>
          <td> present</td>
          <td> 1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>21</th>
          <td> present</td>
          <td> 1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>22</th>
          <td> present</td>
          <td> 0</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>23</th>
          <td> present</td>
          <td> 0</td>
          <td> right</td>
        </tr>
        <tr>
          <th>24</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>25</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>26</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>27</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>28</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>29</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
        <tr>
          <th>30</th>
          <td> neutral</td>
          <td>-1</td>
          <td>  left</td>
        </tr>
        <tr>
          <th>31</th>
          <td> neutral</td>
          <td>-1</td>
          <td> right</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    posner_full = extend(posner, max_length = 390, rep_ix = 'iteration')
    len(posner_full)



.. parsed-literal::

    384



add\_block
----------

                .. autofunction:: labtools.trials_functions.add_block
    :noindex:
                
simple\_shuffle
---------------

                .. autofunction:: labtools.trials_functions.simple_shuffle
    :noindex:
                
smart\_shuffle
--------------

                .. autofunction:: labtools.trials_functions.smart_shuffle
    :noindex:
                
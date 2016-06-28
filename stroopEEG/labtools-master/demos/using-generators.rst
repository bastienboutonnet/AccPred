
Using Generators
================

This demo exhibits some of the advantages to using generators for more
complicated trial generation.

.. code:: python

    # this demo is in the root dir of the labtools project, available on GitHub
    import sys, os
    sys.path.insert(0, os.path.abspath('..'))
    
    import pandas as pd
    import numpy as np
    
    from labtools.trials_functions import *
    from labtools.generator_functions import *

.. parsed-literal::

    /Users/edmiston/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/pandas/io/excel.py:626: UserWarning: Installed openpyxl is not supported at this time. Use >=1.6.1 and <2.0.0.
      .format(openpyxl_compat.start_ver, openpyxl_compat.stop_ver))


.. code:: python

    items = ['red','orange','yellow','green','blue','indigo','violet']
    items = pd.DataFrame({'item':items}, index = pd.Index(range(len(items)),
                                                          name = 'item_id'))
    
    stroop = pd.DataFrame({'letters':items['item'].values})
    stroop = extend(stroop, reps = 4, rep_ix = 'letters_iter', 
                    row_ix = 'letters_id')
    stroop



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>letters_iter</th>
          <th>letters_id</th>
          <th>letters</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0 </th>
          <td> 0</td>
          <td> 0</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>1 </th>
          <td> 0</td>
          <td> 1</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>2 </th>
          <td> 0</td>
          <td> 2</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>3 </th>
          <td> 0</td>
          <td> 3</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>4 </th>
          <td> 0</td>
          <td> 4</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>5 </th>
          <td> 0</td>
          <td> 5</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>6 </th>
          <td> 0</td>
          <td> 6</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>7 </th>
          <td> 1</td>
          <td> 0</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>8 </th>
          <td> 1</td>
          <td> 1</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>9 </th>
          <td> 1</td>
          <td> 2</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>10</th>
          <td> 1</td>
          <td> 3</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>11</th>
          <td> 1</td>
          <td> 4</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>12</th>
          <td> 1</td>
          <td> 5</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>13</th>
          <td> 1</td>
          <td> 6</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>14</th>
          <td> 2</td>
          <td> 0</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>15</th>
          <td> 2</td>
          <td> 1</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>16</th>
          <td> 2</td>
          <td> 2</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>17</th>
          <td> 2</td>
          <td> 3</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>18</th>
          <td> 2</td>
          <td> 4</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>19</th>
          <td> 2</td>
          <td> 5</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>20</th>
          <td> 2</td>
          <td> 6</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>21</th>
          <td> 3</td>
          <td> 0</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>22</th>
          <td> 3</td>
          <td> 1</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>23</th>
          <td> 3</td>
          <td> 2</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>24</th>
          <td> 3</td>
          <td> 3</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>25</th>
          <td> 3</td>
          <td> 4</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>26</th>
          <td> 3</td>
          <td> 5</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>27</th>
          <td> 3</td>
          <td> 6</td>
          <td> violet</td>
        </tr>
      </tbody>
    </table>
    </div>



*circular*\ generator
---------------------

The basic workhorse of the generator functions is a generator that
yields rows from a ``pandas.DataFrame`` circularly, i.e., once you get
to the bottom, you go back to the top of the list. However, it doesn't
do much on it's own, so it's a private function in the ``labtools``
package.

                .. autofunction:: labtools.generator_functions._circular_generator
    :noindex:
                
generate
--------

``generate`` is the lowest level of trial generation. You have a trial
list, and a source. ``generate`` takes from the source and adds to the
trial list.

                .. autofunction:: labtools.generator_functions.generate
    :noindex:
                
.. code:: python

    generate(stroop, items, source_cols = {'item':'color'}, seed = 123)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>letters_iter</th>
          <th>letters_id</th>
          <th>letters</th>
          <th>color</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0 </th>
          <td> 0</td>
          <td> 0</td>
          <td>    red</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>1 </th>
          <td> 0</td>
          <td> 1</td>
          <td> orange</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>2 </th>
          <td> 0</td>
          <td> 2</td>
          <td> yellow</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>3 </th>
          <td> 0</td>
          <td> 3</td>
          <td>  green</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>4 </th>
          <td> 0</td>
          <td> 4</td>
          <td>   blue</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>5 </th>
          <td> 0</td>
          <td> 5</td>
          <td> indigo</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>6 </th>
          <td> 0</td>
          <td> 6</td>
          <td> violet</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>7 </th>
          <td> 1</td>
          <td> 0</td>
          <td>    red</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>8 </th>
          <td> 1</td>
          <td> 1</td>
          <td> orange</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>9 </th>
          <td> 1</td>
          <td> 2</td>
          <td> yellow</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>10</th>
          <td> 1</td>
          <td> 3</td>
          <td>  green</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>11</th>
          <td> 1</td>
          <td> 4</td>
          <td>   blue</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>12</th>
          <td> 1</td>
          <td> 5</td>
          <td> indigo</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>13</th>
          <td> 1</td>
          <td> 6</td>
          <td> violet</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>14</th>
          <td> 2</td>
          <td> 0</td>
          <td>    red</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>15</th>
          <td> 2</td>
          <td> 1</td>
          <td> orange</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>16</th>
          <td> 2</td>
          <td> 2</td>
          <td> yellow</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>17</th>
          <td> 2</td>
          <td> 3</td>
          <td>  green</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>18</th>
          <td> 2</td>
          <td> 4</td>
          <td>   blue</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>19</th>
          <td> 2</td>
          <td> 5</td>
          <td> indigo</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>20</th>
          <td> 2</td>
          <td> 6</td>
          <td> violet</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>21</th>
          <td> 3</td>
          <td> 0</td>
          <td>    red</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>22</th>
          <td> 3</td>
          <td> 1</td>
          <td> orange</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>23</th>
          <td> 3</td>
          <td> 2</td>
          <td> yellow</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>24</th>
          <td> 3</td>
          <td> 3</td>
          <td>  green</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>25</th>
          <td> 3</td>
          <td> 4</td>
          <td>   blue</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>26</th>
          <td> 3</td>
          <td> 5</td>
          <td> indigo</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>27</th>
          <td> 3</td>
          <td> 6</td>
          <td> violet</td>
          <td> orange</td>
        </tr>
      </tbody>
    </table>
    </div>



generate\_but\_not
------------------

However, often you won't just want to randomly stick together your trial
list with some source, as in the case of a Stroop experiment. We want to
be able to control which letters go with which colors so that they don't
match. Building on ``generate`` is the function ``generate_but_not``
which breaks the trial list into chunks before using
``_circular_generator``\ s.

                .. autofunction:: labtools.generator_functions.generate_but_not
    :noindex:
                
.. code:: python

    generate_but_not(stroop, items, on = ['letters','item'],
                     source_cols = {'item':'color'}, seed = 124)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>letters_iter</th>
          <th>letters_id</th>
          <th>letters</th>
          <th>color</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0 </th>
          <td> 0</td>
          <td> 0</td>
          <td>    red</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>1 </th>
          <td> 0</td>
          <td> 1</td>
          <td> orange</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>2 </th>
          <td> 0</td>
          <td> 2</td>
          <td> yellow</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>3 </th>
          <td> 0</td>
          <td> 3</td>
          <td>  green</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>4 </th>
          <td> 0</td>
          <td> 4</td>
          <td>   blue</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>5 </th>
          <td> 0</td>
          <td> 5</td>
          <td> indigo</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>6 </th>
          <td> 0</td>
          <td> 6</td>
          <td> violet</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>7 </th>
          <td> 1</td>
          <td> 0</td>
          <td>    red</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>8 </th>
          <td> 1</td>
          <td> 1</td>
          <td> orange</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>9 </th>
          <td> 1</td>
          <td> 2</td>
          <td> yellow</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>10</th>
          <td> 1</td>
          <td> 3</td>
          <td>  green</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>11</th>
          <td> 1</td>
          <td> 4</td>
          <td>   blue</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>12</th>
          <td> 1</td>
          <td> 5</td>
          <td> indigo</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>13</th>
          <td> 1</td>
          <td> 6</td>
          <td> violet</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>14</th>
          <td> 2</td>
          <td> 0</td>
          <td>    red</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>15</th>
          <td> 2</td>
          <td> 1</td>
          <td> orange</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>16</th>
          <td> 2</td>
          <td> 2</td>
          <td> yellow</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>17</th>
          <td> 2</td>
          <td> 3</td>
          <td>  green</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>18</th>
          <td> 2</td>
          <td> 4</td>
          <td>   blue</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>19</th>
          <td> 2</td>
          <td> 5</td>
          <td> indigo</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>20</th>
          <td> 2</td>
          <td> 6</td>
          <td> violet</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>21</th>
          <td> 3</td>
          <td> 0</td>
          <td>    red</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>22</th>
          <td> 3</td>
          <td> 1</td>
          <td> orange</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>23</th>
          <td> 3</td>
          <td> 2</td>
          <td> yellow</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>24</th>
          <td> 3</td>
          <td> 3</td>
          <td>  green</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>25</th>
          <td> 3</td>
          <td> 4</td>
          <td>   blue</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>26</th>
          <td> 3</td>
          <td> 5</td>
          <td> indigo</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>27</th>
          <td> 3</td>
          <td> 6</td>
          <td> violet</td>
          <td>   blue</td>
        </tr>
      </tbody>
    </table>
    </div>



generate\_matches
-----------------

Although trivially easy in the case of a Stroop task, we can also do the
reverse using ``generate_matches``.

                .. autofunction:: labtools.generator_functions.generate_matches
    :noindex:
                
.. code:: python

    generate_matches(stroop, items, on = ['letters','item'],
                     source_cols = {'item':'color'}, seed = 124)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>letters_iter</th>
          <th>letters_id</th>
          <th>letters</th>
          <th>color</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0 </th>
          <td> 0</td>
          <td> 0</td>
          <td>    red</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>1 </th>
          <td> 0</td>
          <td> 1</td>
          <td> orange</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>2 </th>
          <td> 0</td>
          <td> 2</td>
          <td> yellow</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>3 </th>
          <td> 0</td>
          <td> 3</td>
          <td>  green</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>4 </th>
          <td> 0</td>
          <td> 4</td>
          <td>   blue</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>5 </th>
          <td> 0</td>
          <td> 5</td>
          <td> indigo</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>6 </th>
          <td> 0</td>
          <td> 6</td>
          <td> violet</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>7 </th>
          <td> 1</td>
          <td> 0</td>
          <td>    red</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>8 </th>
          <td> 1</td>
          <td> 1</td>
          <td> orange</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>9 </th>
          <td> 1</td>
          <td> 2</td>
          <td> yellow</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>10</th>
          <td> 1</td>
          <td> 3</td>
          <td>  green</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>11</th>
          <td> 1</td>
          <td> 4</td>
          <td>   blue</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>12</th>
          <td> 1</td>
          <td> 5</td>
          <td> indigo</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>13</th>
          <td> 1</td>
          <td> 6</td>
          <td> violet</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>14</th>
          <td> 2</td>
          <td> 0</td>
          <td>    red</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>15</th>
          <td> 2</td>
          <td> 1</td>
          <td> orange</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>16</th>
          <td> 2</td>
          <td> 2</td>
          <td> yellow</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>17</th>
          <td> 2</td>
          <td> 3</td>
          <td>  green</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>18</th>
          <td> 2</td>
          <td> 4</td>
          <td>   blue</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>19</th>
          <td> 2</td>
          <td> 5</td>
          <td> indigo</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>20</th>
          <td> 2</td>
          <td> 6</td>
          <td> violet</td>
          <td> violet</td>
        </tr>
        <tr>
          <th>21</th>
          <td> 3</td>
          <td> 0</td>
          <td>    red</td>
          <td>    red</td>
        </tr>
        <tr>
          <th>22</th>
          <td> 3</td>
          <td> 1</td>
          <td> orange</td>
          <td> orange</td>
        </tr>
        <tr>
          <th>23</th>
          <td> 3</td>
          <td> 2</td>
          <td> yellow</td>
          <td> yellow</td>
        </tr>
        <tr>
          <th>24</th>
          <td> 3</td>
          <td> 3</td>
          <td>  green</td>
          <td>  green</td>
        </tr>
        <tr>
          <th>25</th>
          <td> 3</td>
          <td> 4</td>
          <td>   blue</td>
          <td>   blue</td>
        </tr>
        <tr>
          <th>26</th>
          <td> 3</td>
          <td> 5</td>
          <td> indigo</td>
          <td> indigo</td>
        </tr>
        <tr>
          <th>27</th>
          <td> 3</td>
          <td> 6</td>
          <td> violet</td>
          <td> violet</td>
        </tr>
      </tbody>
    </table>
    </div>



Generic functions
=================

More complicated generation can be accomplished by using the two
workhorse functions ``generate_by_group`` and ``create_source_map``.

generate\_by\_group
-------------------

                .. autofunction:: labtools.generator_functions.generate_by_group
    :noindex:
                
create\_source\_map
-------------------

                .. autofunction:: labtools.generator_functions.create_source_map
    :noindex:
                
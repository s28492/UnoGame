import pytest
import pandas as pd
import sys
import os
from Uno.DecisionTrees.ID3Tree import calculate_entropy_numba
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/Uno/DecisionTrees/ID3Tree.py')))
@pytest.fixture
def calculate_entropy_numba():

    empty_df = pd.DataFrame()
    empty_series = pd.Series()
    one_row_df = pd.DataFrame(columns=['col1', 'col2', 'col3'], data=[1, 2, 3])
    one_element_series = pd.Series([1])
    assert calculate_entropy_numba(empty_df, empty_series) == 0
    assert calculate_entropy_numba(one_row_df, one_element_series) == 0


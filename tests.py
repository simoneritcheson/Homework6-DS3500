import pytest
import pandas as pd
from ta import overallocation, time_conflict, undersupport
from ta import max_assigned, times, section_data ##Imports for data

# read in test csvs
@pytest.fixture
def sample_solutions():
    test_1 = (pd.read_csv('test1.csv', header=None)).to_numpy()
    test_2 = (pd.read_csv('test2.csv', header=None)).to_numpy()
    test_3 = (pd.read_csv('test3.csv', header=None)).to_numpy()
    return test_1, test_2, test_3


def test_overallocation(sample_solutions):
    test_1, test_2, test_3 = sample_solutions
    assert overallocation(test_1, max_assigned) == 37
    assert overallocation(test_2, max_assigned) == 41
    assert overallocation(test_3, max_assigned) == 23

def test_timeconflict(sample_solutions):
    test_1, test_2, test_3 = sample_solutions
    assert time_conflict(test_1, times) == 42
    assert time_conflict(test_2, times) == 43
    assert time_conflict(test_3, times) == 44

def test_undersupport(sample_solutions):
    test_1, test_2, test_3 = sample_solutions
    assert undersupport(test_1, section_data) == 1
    assert undersupport(test_2, section_data) == 0
    assert undersupport(test_3, section_data) == 7


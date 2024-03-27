import pandas as pd
from ta import overallocation, max_assigned

# read in test csvs
test_1 = (pd.read_csv('test1.csv')).to_numpy()
test_2 = (pd.read_csv('test2.csv')).to_numpy()
test_3 = (pd.read_csv('test3.csv')).to_numpy()

def test_overallocation(test_csv, max_assigned, expected):
    """
    Test the overallocation objective function
    :param test_csv: Example solution
    :param max_assigned: Array with the max_assigned information for each TA
    :param expected: The expected output as specified in the assignment
    :return: Test case passed/failed
    """
    # Get the actual output
    actual = overallocation(test_csv, max_assigned)

    # Assert that the actual output is the same as the expected output
    assert actual == expected


test_overallocation(test_2, max_assigned, 41)


import pandas as pd
import numpy as np
import pytest

tas_df = pd.read_csv('tas.csv')
sections_df = pd.read_csv('sections.csv')

# Process TA Data
# Assume columns 0 to 16 in tas_df correspond to availability and preference
ta_data = tas_df.iloc[:, 3:].replace({'U': 0, 'W': 1, 'P': 2}).values

# we still need max_assigned information for each TA:
def max_assigned(tas_df):
    return tas_df['max_assigned'].values
max_assigned = max_assigned(tas_df)

# Isolate time information for each practicum section
def times(sections_df):
    return sections_df['daytime'].values
times = times(sections_df)

# Process Section Data
def section_data(sections_df):
    # Extract the 'min_ta' and 'max_ta' columns from sections_df
    min_ta = sections_df['min_ta'].values
    max_ta = sections_df['max_ta'].values
    # Have baby arrays in big array [min, max]
    return np.column_stack((min_ta, max_ta))

section_data = section_data(sections_df)
# Combine Data
num_tas = len(ta_data)
num_sections = len(section_data)

# initialize our solution data structure by having each array (row) represent a ta and each column (or index in that array) represent a lab practicum
# just initialize it by randomly filling the array's with 0 or 1 (they are assigned or not assigned) and then we will make them better

data_arrays = [np.random.randint(2, size=num_sections) for _ in range(num_tas)]

# Combine the individual arrays into a single data structure
data = np.array(data_arrays)

# before we do objectives/agents, function should assign ta's to section.
# loop through different lists within the list, assign a random number from the TA options
# start by randomly assigning them to a practicum with no consideration for their preferences



# Add objectives below


def overallocation(data, max_assigned):
    """
    If a TA requests at most 2 labs and you assign to them 5 labs, that’s an overallocation penalty of 3.
    Compute the objective by summing the overallocation penalty over all TAs. There is no minimum allocation

    :param data: The solution dataframe with each row representing a TA and each column representing a lab section.
    :param max_assigned: An array with 1 value per TA indicating the maximum amount of lab practicums that TA can be assigned to.
    :return: Total penalty value.
    """

    return sum([num_assigned - max_assigned[i] for i, num_assigned in enumerate(map(sum, data)) if num_assigned > max_assigned[i]])

def undersupport(data, section_data):
    """
    If a section needs at least 3 TAs and you only assign 1, count that as 2 penalty points.
    Minimize the total penalty score across all sections. No penalty for too many TAs.

    :param data: The solution dataframe with each row representing a TA and each column representing a lab section.
    :param section_data: A 2D array containing arrays for each lab practicum representing the min and max amount of TAs required.
    :return: A penalty score.
    """

    # get number of TA's assigned to each lab practicum
    num_ones_per_column = np.sum(data, axis=0)

    # get penalty scores by matching up corresponding indeces in the num_ones_per_column and section_data arrays
    # only consider a penalty score when the value in num_ones_per_column is less than the first element in the inner array of section_data
    penalties = sum([section_value - num_ones if num_ones < section_value else 0 for num_ones, section_value in
                 zip(num_ones_per_column, section_data[:, 0])]) # section_data[:, 0] selects all the min_amounts

    return penalties

def time_conflict(data, times):
    """
ADD DOCSTRING
    :param data: 
    :param times: 
    :return: 
    """
    penalty = 0
    for i in range(len(data)):
        ta_array = data[i]
        indices = np.where(ta_array==1)[0]
        #print('this is indeces: ', indices)
        selected_times = times[indices]
        # Check if there's a conflict 
        has_conflict = len(selected_times) != len(np.unique(selected_times))
        #print("Is there a time conflict?", has_conflict)
        if has_conflict:
            penalty += 1
    return penalty




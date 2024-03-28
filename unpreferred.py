import pandas as pd
import numpy as np


tas_df = pd.read_csv('tas.csv')
sections_df = pd.read_csv('sections.csv')
solution = np.array([
    [1, 0, 1],  # TA 1 is assigned to sections 0 and 2
    [0, 1, 0],  # TA 2 is assigned to section 1
    [1, 1, 0],  # TA 3 is assigned to sections 0 and 1
])

# Process TA Data
# Assume columns 0 to 16 in tas_df correspond to availability and preference
ta_data = tas_df.iloc[:, 3:].replace({'U': 0, 'W': 1, 'P': 2}).values

# we still need max_assigned information for each TA:
def max_assigned(tas_df):
    return tas_df['max_assigned'].values
max_assigned = max_assigned(tas_df)
# what we will have to do with max_assigned: # loop through and see when a TA id is assigned too many times, correspond it to max_assigned index

# Process Section Data
# Extract the 'min_ta' and 'max_ta' columns from sections_df
min_ta = sections_df['min_ta'].values
max_ta = sections_df['max_ta'].values
# make sure it's not going over the max number. have baby arrays in big array [min, max]
section_data = np.column_stack((min_ta, max_ta))

times = sections_df['daytime'].values

# Combine Data
num_tas = len(ta_data)
num_sections = len(section_data)

# initialize our solution data structure by having each array (row) represent a ta and each column (or index in that array) represent a lab practicum
# just initialize it by randomly filling the array's with 0 or 1 (they are assigned or not assigned) and then we will make them better

data_arrays = [np.random.randint(2, size=num_sections) for _ in range(num_tas)]

# Combine the individual arrays into a single data structure
data = np.array(data_arrays)

# Add objectives below


#def overallocation(data, max_assigned):
   # """ If a TA requests at most 2 labs and you assign to them 5 labs, that’s an overallocation penalty of 3.
   # Compute the objective by summing the overallocation penalty over all TAs. There is no minimum allocation"""

    #return sum([num_assigned - max_assigned[i] for i, num_assigned in enumerate(map(sum, data)) if num_assigned > max_assigned[i]])


# Define the fitness function
def unpreferred(solution, tas_df):
    """
    Calculate the fitness of the solution based on the number of times TAs are allocated
    to sections where they are willing but not preferred.

    Parameters:
    solution (np.ndarray): Binary array representing the solution where each element indicates
                           whether a TA is assigned to a section (1) or not (0).
    Returns:
    float: Fitness value of the solution. Lower values indicate better fitness.
    """
    # this was my original function, it is now not working so I went about it another way on line 73
    # Calculate unpreferred count using list comprehension
    #unpreferred_count = sum(1 for idx, ta_row in tas_df.iterrows() for section, preference in ta_row.items() if
                         #  preference == 'W' and solution[int(section) - 1] == 1 and int(section) - 1 < len(solution))
    #return unpreferred_count


    return sum(1 for idx, ta_row in tas_df.iterrows() for section, preference in ta_row.items() if
               preference == 'W' and any(preference != 'U' for preference in ta_row[2:]) and ta_row[section] == 'W')

# Call the unpreferred function with the solution array and tas_df
unpreferred_count = unpreferred(solution, tas_df)

# Print the result
print("the unpreferred count is:", unpreferred_count)
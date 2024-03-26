import pandas as pd
import numpy as np

tas_df = pd.read_csv('tas.csv')
sections_df = pd.read_csv('sections.csv')

# Process TA Data
# Assume columns 0 to 16 in tas_df correspond to availability and preference
ta_data = tas_df.iloc[:, 3:].replace({'U': 0, 'W': 1, 'P': 2}).values

# we still need max_assigned information for each TA:
max_assigned = tas_df['max_assigned'].values
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

# before we do objectives/agents, function should assign ta's to section.
# loop through different lists within the list, assign a random number from the TA options
# start by randomly assigning them to a practicum with no consideration for their preferences

# agents optimize as it runs
print(times)
print(section_data)




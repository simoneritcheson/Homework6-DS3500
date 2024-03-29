import pandas as pd
import numpy as np
import evo
import random as rnd

tas_df = pd.read_csv('tas.csv')
sections_df = pd.read_csv('sections.csv')
section_prefs = tas_df.iloc[0:, 3:].values
allocation = tas_df["max_assigned"].values

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
print(data)


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

    return sum([num_assigned - max_assigned[i] for i, num_assigned in enumerate(map(sum, data)) if
                num_assigned > max_assigned[i]])


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
                     zip(num_ones_per_column, section_data[:, 0])])  # section_data[:, 0] selects all the min_amounts

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
        indices = np.where(ta_array == 1)[0]
        # print('this is indeces: ', indices)
        selected_times = times[indices]
        # Check if there's a conflict 
        has_conflict = len(selected_times) != len(np.unique(selected_times))
        # print("Is there a time conflict?", has_conflict)
        if has_conflict:
            penalty += 1
    return penalty


def unwilling(data):
    unwilling_lst =  np.where((data == 1) & (section_prefs == 'U'), 1, 0)
    unwilling_count = [sum(lst) for lst in unwilling_lst]
    return sum(unwilling_count)

def allocate(data):
    """
    finding which ta's are overallocared and swapping the index of an assigned
    :param solutions: numpy array, one solution
    :return: update solutions
    """

    new_solution = np.copy(data)

    #list of position in sol of each ta who is overallocated
    overallocated_tas = [i for i, ta_assignments in enumerate(data) if np.sum(ta_assignments) > allocation[i]]

    # if no tas overallocated
    if not overallocated_tas:
        return new_solution

    # Choose a random overallocated TA
    selected_ta_index = rnd.choice(overallocated_tas)
    selected_ta_assignments = new_solution[selected_ta_index]

    # Find indices of sections assigned to the selected TA
    assigned_sections_indices = np.where(selected_ta_assignments == 1)[0]

    # If no sections are assigned to the selected TA, return the original solution
    if not assigned_sections_indices:
        return new_solution

    # Choose a random section assigned to the selected TA
    selected_section_index = rnd.choice(assigned_sections_indices)

    # Reallocate the selected section by unassigning it from the selected TA
    new_solution[selected_ta_index][selected_section_index] = 0

    return new_solution

def trade_rows(data):
    """
    swaps one row of solution with another solutions row (swap TA assignment)
    param solutions: numpy array, one solution
    :return: new solution generated from original
    """
    #accesses first solution
    solution_1, solution_2 = np.copy(data[0]), np.copy(data[1])

    row_index = rnd.randrange(0, len(solution_1))

    # Swap the selected row between the two solutions
    solution_1[row_index], solution_2[row_index] = solution_2[row_index], solution_1[row_index]

    # Return the updated solutions
    return np.array([solution_1, solution_2])


def main():
    # create the environment
    E = evo.Environment()

    # register the fitness functions
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("timeconflict", time_conflict)
    #E.add_fitness_criteria("underpreferred", underpreferred) # SIMONE ADD TO TA.PY

    # register agents
    #E.add_agent("allocate", allocate, 1)
   # E.add_agent("traderows", trade_rows, 1)


    data = np.array(data_arrays)
    E.add_solution(data)

    # run the evolver
    E.evolve(1, 100, 1)  # this is saying (run  ___ iterations, __ , print out results for every __)

    # print the final result
    print(E)


if __name__ == '__main__':
    main()
print(data)

"""
File: ta.py
Description: Formats csv data and establishes objective and agent functions.
"""
import pandas as pd
import numpy as np
import evo
import random as rnd
import time

# Read in csv's
tas_df = pd.read_csv('tas.csv')
sections_df = pd.read_csv('sections.csv')

# Create a
section_prefs = tas_df.iloc[0:, 3:].values
allocation = tas_df["max_assigned"].values
# Process TA Data
# Assume columns 0 to 16 in tas_df correspond to availability and preference
ta_data = tas_df.iloc[:, 3:].replace({'U': 0, 'W': 1, 'P': 2}).values


# we still need max_assigned information for each TA
max_assigned = tas_df['max_assigned'].values


# Isolate time information for each practicum section
times = sections_df['daytime'].values


# Process Section Data

# Extract the 'min_ta' and 'max_ta' columns from sections_df
min_ta = sections_df['min_ta'].values
max_ta = sections_df['max_ta'].values

# Have baby arrays in big array [min, max]
section_data = np.column_stack((min_ta, max_ta))

# Combine Data
num_tas = len(ta_data)
num_sections = len(section_data)

# Initalize the data by randomly filling the array's with 0 or 1 (they are assigned or not assigned)
data_arrays = [np.random.randint(2, size=num_sections) for _ in range(num_tas)]

# Combine the individual arrays into a single data structure
data = np.array(data_arrays)

# Add objectives below

def overallocation(data):
    """
    If a TA requests at most 2 labs and you assign to them 5 labs, that’s an overallocation penalty of 3.
    Compute the objective by summing the overallocation penalty over all TAs. There is no minimum allocation

    :param data: The solution dataframe with each row representing a TA and each column representing a lab section.
    :return: Total penalty value.
    """

    return sum([num_assigned - max_assigned[i] for i, num_assigned in enumerate(map(sum, data)) if
                num_assigned > max_assigned[i]])


def undersupport(data):
    """
    If a section needs at least 3 TAs and you only assign 1, count that as 2 penalty points.
    Minimize the total penalty score across all sections. No penalty for too many TAs.

    :param data: The solution dataframe with each row representing a TA and each column representing a lab section.
    :return: A penalty score.
    """

    # get number of TA's assigned to each lab practicum
    num_ones_per_column = np.sum(data, axis=0)

    # get penalty scores by matching up corresponding indeces in the num_ones_per_column and section_data arrays
    # only consider a penalty when the value in num_ones_per_column is less than the first element in the inner array of section_data
    penalties = sum([section_value - num_ones if num_ones < section_value else 0 for num_ones, section_value in
                     zip(num_ones_per_column, section_data[:, 0])])  # section_data[:, 0] selects all the min_amounts

    return penalties


def time_conflict(data):
    """
    Calculate the number of time conflicts for assigned TAs.
    A time conflict occurs when a TA is assigned to multiple sections that meet at the same time.

    :param data: A 2D numpy array where each row represents a TA and each column represents a lab section.
        A value of 1 indicates the TA is assigned to that section.
    :return: The total number of TAs with time conflicts.
    """
    penalty = sum([
        1 for ta_array in data if len(set(times[np.where(ta_array == 1)[0]])) != np.sum(ta_array)
    ])
    return penalty


def unwilling(data):
    """
    Find and return the number of times a TA is assigned to a section where they are unwilling

    :param data: A 2D numpy array where each row represents a TA and each column represents a lab
    :return:  an int indicating the number of "unwilling" assignments. Lower values indicate better fitness.
    """
    unwilling_lst = np.where((data == 1) & (section_prefs == 'U'), 1, 0)
    unwilling_count = [sum(lst) for lst in unwilling_lst]
    return sum(unwilling_count)


def unpreferred(data):
    """
    Calculate the fitness of the solution based on the number of times TAs are allocated
    to sections where they are willing but not preferred.

    :param data: Binary array representing the solution where each element indicates
                           whether a TA is assigned to a section (1) or not (0).

    :return: Fitness value of the solution. Lower values indicate better fitness.
        """
    unpreferred_lst = np.where((data == 1) & (section_prefs == 'W'), 1, 0)
    unpreferred_count = [sum(lst) for lst in unpreferred_lst]
    return sum(unpreferred_count)


def allocate(data):
    """
    Optimize allocated TAs

    :param data: (numpy array) data of solutions
    :return: new array of solutions
    """

    new_solution = np.copy(data)

    # list of position in sol of each ta who is overallocated
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

# Add agents

def swap_tas(data):
    """
    Change rows, essentially randomly changing TA assignments
    :param data: (numpy array) data of solutions
    :return: new array of solutions
    """
    # accesses first solution
    solution_1, solution_2 = np.copy(data[0]), np.copy(data[1])

    row_index = rnd.randrange(0, len(solution_1))

    # Swap the selected row between the two solutions
    solution_1[row_index], solution_2[row_index] = solution_2[row_index], solution_1[row_index]

    # Return the updated solutions
    return np.array([solution_1, solution_2])


def apply_random(data):
    """
    Mutation agent that toggles a random TA/Lab assignment

    :param data: data of solutions
    :return: new array of solutions
    """
    new_solution = np.copy(data)

    # Choose a random TA index and a random lab section index
    random_ta_index = rnd.randint(0, len(data) - 1)
    random_lab_index = rnd.randint(0, len(data[random_ta_index]) - 1)

    # Toggle the assignment (0 to 1 or 1 to 0)
    new_solution[random_ta_index, random_lab_index] = 1 - new_solution[random_ta_index, random_lab_index]

    return new_solution


def main():

    #group name
    groupname = 'vaas'

    # create the environment
    E = evo.Environment()

    # register the fitness functions
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("time_conflict", time_conflict)
    E.add_fitness_criteria("unpreferred", unpreferred)
    E.add_fitness_criteria("undersupport", undersupport)

    # register agents
    E.add_agent("allocate", allocate, 1)
    E.add_agent("swap_tas", swap_tas, 1)
    E.add_agent("apply_random", apply_random, 1)

    E.add_solution(data)

    # Get the start time
    start_time = time.time()

    # run for 10 minutes
    while time.time() - start_time < 600:  # 600 seconds = 10 minutes
        E.evolve(1)  # run one iteration in each loop

    # Generate the summary table
    pareto_solutions = list(E.pop.values())  # get non-dominated Pareto-optimal solutions
    summary_data = []
    for solution in pareto_solutions:
        overallocate = overallocation(solution)
        conflicts = time_conflict(solution)
        undersupport = undersupport(solution)
        unwillingness = unwilling(solution)
        unpreferred = unpreferred(solution)
        summary_data.append([groupname, overallocate, conflicts, undersupport, unwillingness, unpreferred])

    # Save summary table as CSV
    columns = ['groupname', 'overallocation', 'conflicts', 'undersupport', 'unwilling', 'unpreferred']
    summary_df = pd.DataFrame(summary_data, columns=columns)
    summary_df.to_csv('summary_table.csv', index=False)

    # Print final result
    print(E)


if __name__ == '__main__':
    main()
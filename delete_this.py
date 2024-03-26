"""
Example: Sorting without sort.
1. we want to inherit (copy a list)
2.  create variations. swap 2 random elements and swap them
3. how unsorted are these lists? (this is the evaluation). count the step downs: 5, 3, 9, 2, 8, 4 has a total of 13 step downs
"""

import evo
import random as rnd

def stepsdown(L):
    """ 1 hr into friday lecture is really helpful. total the step downs in teh numeric sequence """
    # avoid loops as much as possible. in the homework it needs to be fast and concise
    return sum([x - y for x, y in zip(L, L[1:]) if y < x])

def swapper(solutions):
    """
    an agent that swaps two random values
    """
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L

def main():

    # create the environment
    E = evo.Environment()

    # register the fitness functions
    E.add_fitness_criteria("stepdown", stepsdown)

    # register the agents
    E.add_agent("swapper", swapper, 1) # swapper only takes 1 solution as input

    # adding 1 or more initial solution
    L = [rnd.randrange(1, 99) for _ in range(20)]
    E.add_solution(L)

    # run the evolver
    E.evolve(1, 100, 1) # this is saying (run  ___ iterations, __ , print out results for every __)
    # print the final result
    print(E)

if __name__ == '__main__':
    main()
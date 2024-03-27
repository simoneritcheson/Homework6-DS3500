"""
File: evo.py
Description: An evolutionary computing framework for multi-objective optimization
"""
import random as rnd
import copy # original solution is left unchanged! think of a parent having a child
from functools import reduce

class Environment:
    """
    add documentation
    """
    def __init__(self):
        """ Environment constructor """
        self.pop = {} # the key is evaluation across all objects --> the actual solution.
        self.fitness = {} # objectives/fitness functions. name of function --> f
        self.agents = {} # agents: name of agent --> (operator/function, num_solutions_input)


    def size(self):
        """ The size of the current population """
        return len(self.pop)

    def add_fitness_criteria(self, name, f):
        """ Add/declare an objective function to the framework"""
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ register a named agent with the framework
        name: name of agent
        op: the operator, the function, defines what the agent does
        k: defines the number of input solutions that the operator/agent operates on
        """
        self.agents[name] = (op, k)


    def add_solution(self, sol):
        """ Evaluate and add a solution to the population """
        # we need the key, so we need to evaluate the solution as we add it to the population.
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()]) # this is saying for each name and function in teh list of fitness functions, create a little tuple that adds the name and evaluation
        self.pop[eval] = sol

    def get_random_solution(self, k=1):
        """" Pick k random solutions from the population and return as a list. """
        if self.size() == 0: # if you've killed off all solutions, you can't return anything. this typically won't happen
            return []
        else:
            popvals = tuple(self.pop.values()) # get all the solutions
            # choose a random solution from the tuple k times
            return [copy.deepcopy(rnd.choice(popvals)) for _ in range(k)] # again, this is a random choice. but maybe agents could learn which are better solutions to choose. They could know that they get better results from certain solutions
            # we do deep copy because we might want the og solutiions agian

    def run_agent(self, name):
        """ Pick some random solutions, apply an agent operator to that solution to make a new solution, then add that new solution.
        Usually this is some sort of a mutator that randomly changes the population in some way.
        You can get better results by having a more goal directed agent. Be a little more intelligent and a little less random.
        Extra credit in homework 6 for more intelligent solution.

        param name: i wanna run this agent """
        op, k = self.agents[name]
        picks = self.get_random_solution(k) # get a random number of solutions

        # now make a new solution with the agent
        new_solution = op(picks)
        self.add_solution(new_solution)

    @staticmethod
    def _dominates(p, q):
        """" p and q are the evaluations of the solutions, not th eactual solutions themselves """
        # extracting out all the scores, computing all the differences.
        pscores = [score for _,score in p]
        qscores = [score for _,score in q]
        score_diffs = list(map(lambda x,y: y-x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        # p dominates q if p is at least as good as q with respect to every objective, and strictly better than q in at least 1 objective.
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        """ S is set of solutions, p is point"""
        return S - {q for q in S if Environment._dominates(p,q)} # if something is dominated remove it


    def remove_dominated(self):
        """ check out jupyter notebook that has reduce approach """
        # nds = non dominated solutions
        nds = reduce(Environment._reduce_nds, self.pop.keys(), self.pop.keys()) # starting set is self.pop.keys()
        self.pop = {k:self.pop[k] for k in nds} # new population dictionary with all the non-dominated solutions

    def evolve(self, n=1, dom=100, status=100):
        agent_names = list(self.agents.keys())
        for i in range(n):
            # pick an agent name,
            pick = rnd.choice(agent_names)
            # run the agent
            self.run_agent(pick)
            if i % dom == 0: # if we've hit the amount of cycles we want to check if it dominates
                self.remove_dominated()
            if i % status == 0:
                print("Iteration:", i)
                print("Popoulation size: ", self.size())
                print(self)

        self.remove_dominated() # cleaning up the population one last time

    def __str__(self):
        """ make results a string so u can print it out"""
        rslt = ""
        for eval, sol in self.pop.items():
            rslt += str(dict(eval))+":\t"+str(sol)+"\n"
        return rslt


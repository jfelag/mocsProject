import random

import numpy as np
import config as c
from copy import deepcopy
from ant import Ant
from environment import Environment
import pandas as pd

import matplotlib.pyplot as plt

class Population:
    """
    Handles evolutionary methods for the given object

    Attributes
    ----------
    ind     : class
        the individual type that composes the population
    popSize       : int
        the population size
    p       : dict
        holds the individuals in the population
    fits    : dict
        holds each ants's fitness values

    Methods
    -------
    evaluate()
        evaluates each ant in the population
    """

    def __init__(self, ind, pop_size=10, grid_size=100, steps_per_eval=1000):
        """
        initializes the population of popSize objects
        :param ind: function which returns an instance of the Ant class.
        :param pop_size: number of ants in the population for each evaluation
        :param grid_size: size of grid to simulate on
        :param steps_per_eval: number of steps per evaluation period.
        """

        self.grid_size = grid_size
        self.steps_per_eval = steps_per_eval

        assert isinstance(ind(), Ant), print('ERROR: ind() must return an instance of the Ant class')
        # assert hasattr(ind, 'evaluate'), print('ERROR: Object needs method .evaluate()')

        self.ind = ind
        self.popSize = pop_size
        
        self.p = [None] * self.popSize
        for i in range(self.popSize):
            self.p[i] = self.ind()
            
            
            
    def collect_data(self, t):
        for ant in self.p:
            d = [ant.xPos, ant.yPos, ant.fitness, ant.A, 
                  ant.foodFlag, ant.pVec[0], ant.pVec[1], 
                 ant.pVec[2], t]
            temp = pd.DataFrame.from_dict(data = d)
            try:
                data.append(temp)
            except:
                data = temp
        return data



    def evaluate(self, env):
        """
        evaluates each individual in the population
        :return: None
        """
        # TODO: implement evaluation on the grid. Need to update ant, environment, et al.

        #raise NotImplementedError( "See above TODO note.")
        
        for t in range(c.TIME_STEPS):
            antPositions = self.get_ant_positions()
            data = self.collect_data(t)
            env.update(antPositions)
            self.move(env.grid)
        
            if c.VISUALS:
                
                plt.figure()
                plt.imshow(env.grid, vmin=-10, vmax=10)
                plt.savefig('./figs/fig%03d.png'%t)    
                plt.close()
            
            for ant in self.p:
                
                ant.lifeLeft -= 1
                        
                if ant.get_position() == env.foodPos:
                    ant.foodFlag = 1
                    print('set food flag to 1')
                    ant.timeForFood = t
                    ant.reset_lifetime()
                if ant.get_position() == env.nestPos and ant.foodFlag == 1:
                    ant.nestFlag = 1
                    ant.timeForNest = t
                    
                if ant.lifeLeft == 0:
                    ant.dead = True
                
                
            
        for ant in self.p:
            ant.set_fitness()
            
        data.to_csv('data.csv', mode='a', header=False)                
        

    def selection(self):
        """
        AFPO for genetic evolution
        :return: None
        """
        # increment ages
        for i in range(len(self.p)):
            # print(self.p[i].age, end='->')
            self.p[i].increment_age()
            # print(self.p[i].age)

        # contract the population to non-dominated individuals
        dom_ind = []
        for s in range(len(self.p)):
            dominated = False
            for t in range(len(self.p)):
                if dominates(self.p[t], self.p[s]):
                    dominated = True
                    break
            if not dominated:
                dom_ind.append(self.p[s])
        # TODO: if there are too many dominating individuals then we should randomly kill the ants.
        #       The simlation is probably not robust to changes in number of ants so we must maintain a consistent pop size.

        self.p = dom_ind

        # add new random student
        self.p.append(self.ind())

        # expand the population
        initial_size = len(self.p)
        while len(self.p) < self.popSize:
            parent_index = random.randrange(0, initial_size)
            new_indv = deepcopy(self.p[parent_index])
            new_indv.mutate()
            self.p.append(new_indv)

            
    def getNonDominated(self):

        dom_ind = []
        for s in range(len(self.p)):
            dominated = False
            for t in range(len(self.p)):
                if dominates(self.p[t], self.p[s]):
                    dominated = True
                    break
            if not dominated:
                dom_ind.append(self.p[s])
        return sorted(dom_ind, key=lambda x: x.age)
    
    
    def get_ant_positions(self):
                
        return [(ant.xPos, ant.yPos) for ant in self.p]
    
    
    def move(self, grid):
        
        for ant in self.p:
            if not ant.dead:
                ant.move(grid)
            
    
    def get_fitness(self):
        '''
        '''
        
        return [ant.fitness for ant in self.p]


def dominates(a, b):
    if a.fitness < b.fitness or a.age > b.age:
        return False

    if a.fitness > b.fitness or a.age < b.age:
        return True

    return a.id < b.id

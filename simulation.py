from population import Population
from environment import Environment
import config as c
from ant import Ant
import random
import numpy as np
import pickle

SEED = 0 

random.seed(SEED)
np.random.seed(SEED)

def create_new_ant():
    sensing_area = random.randint(1, 10)
    p_repeat = random.random()
    p_target = random.random()
    p_pheromone = random.random()
    new_ant = Ant(sensing_area, p_repeat, p_target, p_pheromone)
    return new_ant


pop = Population(create_new_ant, pop_size=c.POP_SIZE)
env = Environment(N=c.GRID_SIZE, foodRemaining=c.FOOD_INITIAL)

fitMatrix = np.zeros((c.NUM_GENS, c.POP_SIZE))

for g in range(c.NUM_GENS):
    #reset grid before each simulation
    env.create_grid()
    pop.evaluate(env)
    fitVec = pop.get_fitness()
    print('Generation %03d'%g, fitVec)
    fitMatrix[g] = fitVec
    pop.selection()
    

with open('fitnessValues_%03d.p'%SEED, 'wb') as f:
    
    pickle.dump(fitMatrix, f)
    

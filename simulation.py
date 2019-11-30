from population import Population
from environment import Environment
import config as c
from ant import Ant
import random
import numpy as np


def create_new_ant():
    sensing_area = random.randint(1, 10)
    p_repeat = random.random()
    p_target = random.random()
    p_pheromone = random.random()
    new_ant = Ant(sensing_area, p_repeat, p_target, p_pheromone)
    return new_ant


pop = Population(create_new_ant, pop_size=c.POP_SIZE)
env = Environment(N=c.GRID_SIZE, foodRemaining=c.FOOD_INITIAL)

for i in range(c.NUM_GENS):
    #reset grid before each simulation
    env.create_grid()
    pop.evaluate(env)
    pop.selection()
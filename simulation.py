from population import Population
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

pop = Population(create_new_ant, pop_size = 30)

NUM_GENS = 100

for i in range(100):
    pop.evaluate()
    pop.selection()
from population import Population
from environment import Environment
import config as c
from ant import Ant
import random
import numpy as np
import pickle
import argparse

#def make_args():
#    description = ''
#    parser = argparse.ArgumentParser(description=description,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#    parser.add_argument('-i',
#                        '--inputdir',
#                        help='input directory',
#                        required=True,
#                        type=str)
#    parser.add_argument('-o',
#                        '--outdir',
#                        help='output directory',
#                        required=True,
#                        type=str)
#    parser.add_argument('-s',
#                        '--seed',
#                        help='seed',
#                        required=True,
#                        type=str)
#    return parser.parse_args()


#def main():
#   args = make_args()
#    
#    datadir = args.inputdir
#    outputdir = args.outdir

SEED = 0 

random.seed(SEED)
np.random.seed(SEED)

ANT_ID = 0
def get_ant_id():
    global ANT_ID
    ANT_ID += 1
    return ANT_ID

def create_new_ant():
    sensing_area = random.randint(1, 10)
    p_repeat = random.random()
    p_target = random.random()
    p_pheromone = random.random()
    new_ant = Ant(sensing_area, p_repeat, p_target, p_pheromone, get_id = get_ant_id)
    return new_ant


pop = Population(create_new_ant, pop_size=c.POP_SIZE)
env = Environment(N=c.GRID_SIZE, foodRemaining=c.FOOD_INITIAL)

#fitMatrix = np.zeros((c.NUM_GENS, c.POP_SIZE))

for g in range(c.NUM_GENS):
    if g==c.NUM_GENS-1:
        c.VISUALS = True
    #reset grid before each simulation
    env.create_grid()
    data = pop.evaluate(env)
    fitVec = pop.get_fitness()
    print('Generation %03d'%g, ['%0.3f'%x for x in fitVec])
    #fitMatrix[g] = fitVec
    pop.selection()
    
    data.to_csv('csv/SEED_'+str(SEED)+'_G_'+str(g)+'_.csv')
    

#with open('fitnessValues_%03d.p'%SEED, 'wb') as f:   
    #pickle.dump(fitMatrix, f)
    

#if __name__=="__main__":
#    main()
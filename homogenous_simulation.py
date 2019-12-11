from population import Population
from environment import Environment
import config as c
from ant import Ant
import random
import numpy as np
import pickle
import argparse

def make_args():
    description = ''
    parser = argparse.ArgumentParser(description=description,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s',
                        '--sensing_area',
                        help='sensing_area',
                        required=False,
                        type=int)
    parser.add_argument('-o',
                        '--outdir',
                        help='output directory',
                        required=False,
                        type=str)
    return parser.parse_args()

ANT_ID = 0

def main():
    args = make_args()
    
    SENSING_AREA = args.sensing_area
#    outputdir = args.outdir
    
    SEED_LIST = range(9)
    
    for SEED in SEED_LIST:
    
        random.seed(SEED)
        np.random.seed(SEED)
        
        def get_ant_id():
            global ANT_ID
            ANT_ID += 1
            return ANT_ID
        
        def create_new_ant():
            sensing_area = SENSING_AREA
            p_repeat = random.random()
            p_target = random.random()
            p_pheromone = random.random()
            new_ant = Ant(sensing_area, p_repeat, p_target, p_pheromone, get_id = get_ant_id)
            return new_ant
        
        pop = Population(create_new_ant, pop_size=c.POP_SIZE)
        env = Environment(N=c.GRID_SIZE, foodRemaining=c.FOOD_INITIAL)
                    
        for g in range(c.NUM_GENS):
            if g==c.NUM_GENS-1:
                c.VISUALS = True
            #reset grid before each simulation
            env.create_grid()
            data = pop.evaluate(env)
            fitVec = pop.get_fitness()
            print('Generation %03d'%g, ['%0.3f'%x for x in fitVec])
            pop.selection()
            
            data.to_csv('csv/sensing_area_'+str(SENSING_AREA)+'/SEED_'+str(SEED)+'_G_'+str(g)+'_.csv')


if __name__=="__main__":
    main()

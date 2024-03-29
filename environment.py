import numpy as np
import random
import population
import config as c

if c.VISUALS:
    import matplotlib.pyplot as plt

class Environment:
    
    def __init__(self, N, foodRemaining):
        
        ############# DIMENSIONS AND SIZE #############
        # Dimension of environment
        self.N = N
        # N by N grid defines environment
        self.grid = np.zeros((N, N)) 
        
        ################# FOOD SOURCE #################
        # Food source position (corner)
        self.foodPos = (N-1,N-1)
        # Food remaining in food source
        self.foodRemaining = foodRemaining
        
        #################### NEST #####################
        # Nest source position (other corner)
        self.nestPos = (0,0)
        
        
        
        
    def create_grid(self):
        
        # Create grid
        self.grid = np.zeros((self.N, self.N)) 
        
        # Set food position
        self.foodPos = (self.N-1, self.N-1)
        self.grid[self.foodPos] = c.FOOD_VALUE
        
        # Set nest position
        self.nestPos = (0,0)
        self.grid[self.nestPos] = c.NEST_VALUE
        
        
    
    def update(self, oldPositions):
        
        ############# PHEREMONE DEPLETION #############
     
        self.grid[self.grid<0] += 1
        
        #### PHEREMONE ADDITION AND FOOD CONSUMPTION ####
        for (antPosx, antPosy) in oldPositions:
            
            # Get current ant positions and add pheremones
            if (antPosx, antPosy) != self.nestPos and (antPosx, antPosy) != self.foodPos:
                self.grid[antPosx, antPosy] = -10
            
            # Count how many ants are on a food cell, subtract that number
            # from foodRemaining
            if antPosx == self.N-1 and antPosy == self.N-1:
                self.foodRemaining -= 1
                
        
        ############## MOVE THE POPULATION ##############
        #population.move()
        #NOTE: moved to population.evaluate()
        
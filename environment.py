import numpy as np
import random
import population


class Environment:
    
    def __init__(self, N, foodRemaining):
        
        ############# DIMENSIONS AND SIZE #############
        # Dimension of environment
        self.N = N
        # N by N grid defines environment
        self.grid = np.zeros((N, N)) 
        
        ################# FOOD SOURCE #################
        # Food source position (corner)
        self.foodPos = (N,N)
        # Food remaining in food source
        self.foodRemaining = foodRemaining
        
        #################### NEST #####################
        # Nest source position (other corner)
        self.nestPos = (0,0)
        
        
        
        
    def create_grid(self, N, foodN):
        
        # Create grid
        self.grid = np.zeros((N, N)) 
        
        # Set food position
        self.foodPos = (N,N)
        
        # Set food remaining
        self.foodRemaining = foodN
        
        # Set nest position
        self.nestPos = (0,0)
        
        
        
    
    def update(self):
        
        ############# PHEREMONE DEPLETION #############
        for x in range(self.N):
            for y in range(self.N):
                if self.grid[x][y] < 0:
                    self.grid[x][y] += 1
        
        
        #### PHEREMONE ADDITION AND FOOD CONSUMPTION ####
        oldPositions = population.get_ant_positions()
        for (antPosx, antPosy) in oldPositions:
            
            # Get current ant positions and add pheremones
            self.grid[antPosx][antPosy] += 1
            
            # Count how many ants are on a food cell, subtract that number
            # from foodRemaining
            if antPosx == self.N and antPosy == self.N:
                self.foodRemaining -= 1
        
        
        ############## MOVE THE POPULATION ##############
        population.move()
        
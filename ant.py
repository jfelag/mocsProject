import numpy as np


class Ant:
    
    def __init__(self, A, pR, pT, pP):
        '''
        '''
        
        #variables that store position info
        # # pass these in on initialization?
        self.xPos = 0
        self.yPos = 0
        
        #initialize as 0, set to 1 if food has been found
        self.foodFlag = 0
        
        #ants start with 0, get to 0.5 for partial task completion, 1 for finding food and nest
        self.fitness = 0
        
        #genome 
        # sensing area
        self.A = A
        # repeat step prob
        self.pR = pR
        # target step prob
        self.pT = pT
        # pheromone step prob
        self.pP = pP
        
        
    def move(self, grid):
        '''
        biased walk in same direction as previous step
            or towards food/nest
        '''
        states = getNeighborStates(grid)
        pass
    
    
    def mutate(self):
        '''
        
        '''
        
        pass
    
        
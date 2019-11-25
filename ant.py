import numpy as np

TIME = 100

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
        # repeat step prob, target step prob, pheromone step prob
        self.pVec = np.array([pR, pT, pP])
        
        self.fix_parameters()
        
        
    def move(self, grid):
        '''
        biased walk in same direction as previous step
            or towards food/nest
        '''
        states = self.get_neighbor_states(grid)
        
        if self.foodFlag:
            target = NEST_VALUE
        else:
            target = FOOD_VALUE
        
        states[states==target] = self.pVec[1]
        states[states==PHEROMONE_VALUE] = self.pVec[2]
        
        uStates = states[:self.A, :]
        lStates = states[:, :self.A]
        dStates = states[-self.A:, :]
        rStates = states[:, -self.A:]
        
    
    def get_neighbor_states(self, grid):
        '''
        '''
        N = len(grid)
        xmin = np.min([self.xPos-self.A, 0])
        xmax = np.max([self.xPos+self.A, N-1])
        ymin = np.min([self.yPos-self.A, 0])
        ymax = np.max([self.yPos+self.A, N-1])
        
        squareArea = grid[xmin:xmax+1, ymin:ymax+1]
        
        dist = 2*self.A + 1
        neighbors = np.zeros((dist, dist))
        for x in range(dist):
            for y in range(dist):
                if np.abs(x-self.A)+np.abs(y-self.A) < self.A+1:
                    neighbors[x, y] = 1
                    
        #print(neighbors)
        
        #get cells that are within self.A steps of the ant
        sensedArea = neighbors*squareArea
        
        return sensedArea
        
    
    def get_position(self):
        '''
        '''
        
        return (self.xPos, self.yPos)
    
    
    def mutate(self):
        '''
        
        '''
        
        if np.random.random() < 0.1:
            self.A += np.random.choice([-1, +1])
            if self.A < 1:
                self.A = 1
        else:
            pIdxToChange = np.random.choice([0,1,2])
            #change selected prob to [0.9, 1.1] times its original value
            self.pVec[pIdxToChange] *= 1 + (np.random.random() * 0.2 - 0.1)
            self.pVec /= np.sum(pVec)
        
        self.fix_parameters()
        
    
    def fix_parameters(self):
        '''
        renormalize probability vector to be a valid PMF, and
            update the aliveTime based on sensing area
        '''
        
        self.pVec /= np.sum(pVec)
        
        #smallest sensing area -> alive for half the sim time
        # decrease life by 5 time steps for each bump in radius
        # todo (maybe): change self.A term to quadratic weighting since the sensing area scales like A^2
        self.aliveTime = TIME/2 - 5*self.A + 5
        
        
        
        
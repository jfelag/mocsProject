import numpy as np
import config as c

TIME = 100

class Ant:
    
    def __init__(self, A, pR, pT, pP):
        """

        :param A: Sensing Area
        :param pR: Prob repeat last move
        :param pT:
        :param pP:
        """
        #variables that store position info
        # # pass these in on initialization?
        self.xPos = 0
        self.yPos = 0
        
        #initialize as 0, set to 1 if food has been found
        self.foodFlag = 0
        
        #ants start with 0, get to 0.5 for partial task completion, 1 for finding food and nest
        self.fitness = 0
        
        #initialize last step randomly as right or down
        self.lastStep = np.random.choice(['r','d'])
        
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
        
        N = len(grid)
        
        if self.foodFlag:
            target = c.NEST_VALUE
        else:
            #food value
            target = c.FOOD_VALUE
        
        #bias towards target
        states[states==target] = self.pVec[1]
        #bias towards pheromones
        states[states<0] = self.pVec[2]
        
        uStates = states[:self.A, :]
        lStates = states[:, :self.A]
        dStates = states[-self.A:, :]
        rStates = states[:, -self.A:]
        
        uProb = np.sum(uStates)
        lProb = np.sum(lStates)
        dProb = np.sum(dStates)
        rProb = np.sum(rStates)
        
        #factor in last step bias and add chance to turn
        if self.lastStep == 'r':
            lProb = 0
            rProb += 1+self.pVec[0]
            uProb += 0.5+self.pVec[0]
            dProb += 0.5+self.pVec[0]
        elif self.lastStep == 'l':
            rProb = 0
            lProb += 1+self.pVec[0]
            uProb += 0.5+self.pVec[0]
            dProb += 0.5+self.pVec[0]
        elif self.lastStep == 'u':
            dProb = 0
            uProb += 1+self.pVec[0]
            lProb += 0.5+self.pVec[0]
            rProb += 0.5+self.pVec[0]
        elif self.lastStep == 'd':
            uProb = 0
            dProb += 1+self.pVec[0]
            lProb += 0.5+self.pVec[0]
            rProb += 0.5+self.pVec[0]
        
        #prevent moving outside bounds
        if self.xPos == 0:
            lProb = 0
        if self.xPos == N-1:
            rProb = 0
        if self.yPos == 0:
            uProb = 0
        if self.yPos == N-1:
            dProb = 0
        
        #normalize
        stepVec = np.array([uProb, lProb, dProb, rProb])
        stepVec /= np.sum(stepVec)
        print(stepVec)
        
        #move the ant
        self.lastStep = np.random.choice(['u', 'l', 'd', 'r'], p=stepVec)
        
        if self.lastStep == 'u':
            self.yPos -= 1
        elif self.lastStep == 'l':
            self.xPos -= 1
        elif self.lastStep == 'd':
            self.yPos += 1
        elif self.lastStep == 'r':
            self.xPos += 1

        assert 0 <= self.yPos, "Y pos error"
        assert self.yPos < N, "Y pos error"
        assert 0 <= self.xPos, "x pos error"
        assert self.xPos < N, "x pos error"


    def get_neighbor_states(self, grid):
        '''
        '''
        N = len(grid)
        dist = 2*self.A + 1
        
        xSenseLo = self.xPos-self.A
        xSenseHi = self.xPos+self.A
        ySenseLo = self.yPos-self.A
        ySenseHi = self.yPos+self.A
        xmin = max([xSenseLo, 0])
        xmax = min([xSenseHi, N-1])
        ymin = max([ySenseLo, 0])
        ymax = min([ySenseHi, N-1])
        
        sensedAreaWithBounds = grid[ymin:ymax+1, xmin:xmax+1]
        sensedAreaWithPadding = np.zeros((dist, dist))
        
        #print(sensedAreaWithBounds)
        #print(self.A)
        print()
        print("pos:", self.xPos, self.yPos)
        print("x sense:", xSenseLo, xSenseHi)
        print("y sense:", ySenseLo, ySenseHi)
        print("xmin, xmax, ymin, ymax", xmin, xmax, ymin, ymax)
        print("sense shape:", sensedAreaWithBounds.shape)
        print("target sense shape:", sensedAreaWithPadding.shape)
        
        if xSenseLo < 0:
            if ySenseLo < 0:
                sensedAreaWithPadding[-ySenseLo:, -xSenseLo:] = sensedAreaWithBounds
            elif ySenseHi > N-1:
                sensedAreaWithPadding[:-ySenseHi, -xSenseLo:] = sensedAreaWithBounds 
            else:
                sensedAreaWithPadding[:, -xSenseLo:] = sensedAreaWithBounds 
                
        elif xSenseHi > N-1:
            if ySenseHi > N-1:
                sensedAreaWithPadding[:-ySenseHi, :-xSenseHi] = sensedAreaWithBounds
            elif ySenseLo < 0:
                sensedAreaWithPadding[-ySenseLo:, :-xSenseHi] = sensedAreaWithBounds
            else:
                sensedAreaWithPadding[:, :-xSenseHi] = sensedAreaWithBounds
        else:
            if ySenseLo < 0:
                sensedAreaWithPadding[-ySenseLo:, :] = sensedAreaWithBounds 
            elif ySenseHi > N-1:
                sensedAreaWithPadding[:-ySenseHi, :] = sensedAreaWithBounds 
                

        neighbors = np.zeros((dist, dist))
        for x in range(dist):
            for y in range(dist):
                if abs(x-self.A)+abs(y-self.A) < self.A+1:
                    neighbors[x, y] = 1
                    
        #print(neighbors)
        
        #get cells that are within self.A steps of the ant
        sensedArea = neighbors*sensedAreaWithPadding
        
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
        
        self.pVec /= np.sum(self.pVec)
        
        #smallest sensing area -> alive for half the sim time
        # decrease life by 5 time steps for each bump in radius
        # todo (maybe): change self.A term to quadratic weighting since the sensing area scales like A^2
        self.aliveTime = TIME/2 - 5*self.A + 5
        
        
        
        
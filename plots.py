import pandas as pd
import matplotlib as plt

# Data:
#### ant.xPos - x position
#### ant.yPos - y position
#### ant.fitness - fitness (single number)
#### ant.A - sensing area (integer)
#### ant.foodFlag - boolean
#### ant.pVec[0] - p of repeating a step
#### ant.pVec[1] - p of moving towards food/nest
#### ant.pVec[2] - p of moving towards pheromone
#### t - timestep

data = pd.read_csv('data.csv')

dist_sensing_area0 = data[data['t'] == 0]
plt.hist(dist_sensing_area0['A'], density = True)
plt.title('Distribution of Sensing Area at T = 0')
plt.xlabel('Sensing Area')
plt.ylabel('Frequency')
plt.savefig('figs/dist_sensing_area0.png')

dist_sensing_areaT = data[data['t'] == max(data['t'])]
plt.hist(dist_sensing_areaT['A'], density = True)
plt.title('Distribution of Sensing Area at T = T')
plt.xlabel('Sensing Area')
plt.ylabel('Frequency')
plt.savefig('figs/dist_sensing_areaT.png')

for A in data['A'].unique():
    sensing_area_timeseries = data[data['A'] == A]
    plt.plot(dist_sensing_areaT['A'], density = True)
    
plt.title('Distribution of Sensing Area at T = T')
plt.xlabel('Sensing Area')
plt.ylabel('Frequency')
plt.savefig('figs/dist_sensing_areaT.png')
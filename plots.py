import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
import seaborn as sns

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

data = pd.read_csv('fakedata.csv', index_col=False)
print(data.columns)

# Distribution of # ants by sensing area at T = 0
plt.figure(figsize = (8,6))
dist_sensing_area0 = data[data['t'] == 0]
plt.hist(dist_sensing_area0[' A'], density = True)
plt.title('Distribution of Ant Survival by Sensing Area at T = 0')
plt.xlabel('Sensing Area')
plt.ylabel('Frequency')
plt.xlim(0,max(data[' A']))
plt.savefig('figs/dist_sensing_area0.png')
plt.close()

# Distribution of # ants by sensing area at T = T
plt.figure(figsize = (8,6))
dist_sensing_areaT = data[data['t'] == max(data['t'])]
plt.hist(dist_sensing_areaT[' A'], density = True)
plt.title('Distribution of Ant Survival by Sensing Area at T = T')
plt.xlabel('Sensing Area')
plt.ylabel('Frequency')
plt.xlim(0,max(data[' A']))
plt.savefig('figs/dist_sensing_areaT.png')
plt.close()


# Timeseries of # of ants, each line is a sensing area group
n = len(data[' A'].unique())
colors = pl.cm.jet(np.linspace(0,1,n))
i = 0
plt.figure(figsize = (8,6))
for A in data[' A'].unique():
    sensing_area_timeseries = data[data[' A'] == A].groupby('t').count().reset_index()
    plt.plot(sensing_area_timeseries['t'], sensing_area_timeseries[' A'], color = colors[i])
    i += 1

plt.title('Timeseries for Ant Survival by Sensing Area')
plt.xlabel('Sensing Area')
plt.ylabel('Frequency')
plt.xlim(0,max(data['t']))
plt.savefig('figs/frequency_timeseries.png')
plt.close()


# Timeseries of average fitness, each line is a sensing area group
n = len(data[' A'].unique())
colors = pl.cm.jet(np.linspace(0,1,n))
i = 0
plt.figure(figsize = (8,6))
for A in data[' A'].unique():
    fitness_timeseries = data[data[' A'] == A].groupby('t').mean().reset_index()
    plt.plot(fitness_timeseries['t'], fitness_timeseries[' fitness'], color = colors[i])
    i += 1

plt.title('Timeseries for Average Fitness by Sensing Area')
plt.xlabel('Timesteps')
plt.ylabel('Average Fitness')
plt.xlim(0,max(data['t']))
plt.ylim(0,max(data[' fitness']))
plt.savefig('figs/fitness_timeseries.png')
plt.close()


# Distribution of average fitness by sensing area group
plt.figure(figsize = (8,6))
dist_fitnessT = data[data['t'] == max(data['t'])].groupby(' A').mean().reset_index()
print(dist_fitnessT[' fitness'])
plt.scatter(dist_fitnessT[' A'], dist_fitnessT[' fitness'])
plt.title('Distribution of Average Fitness by Sensing Area at T = T')
plt.xlabel('Sensing Area')
plt.ylabel('Average Fitness')
plt.xlim(0,max(data[' A']))
plt.ylim(0,max(data[' fitness']))
plt.savefig('figs/dist_fitnessT.png')
plt.close()


# Violin plot of each sensing areas fitness distribution
fig = plt.figure()
fig, axes = plt.subplots(figsize = (8,6))
print(min(data[' fitness']))
sns.violinplot(' A',' fitness', data=data, ax = axes)
axes.set_title('Distribution of Fitness by Sensing Area')
#axes.yaxis.grid(True)
axes.set_xlabel('Sensing Area')
axes.set_ylim(0)
axes.set_ylabel('Fitness')

plt.savefig('figs/violin_fitness.png')
plt.close()
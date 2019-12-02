import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
import seaborn as sns
import glob
import argparse

def make_args():
    description = ' '
    parser = argparse.ArgumentParser(description=description,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i',
                        '--inputdir',
                        help='input directory',
                        required=True,
                        type=str)
    parser.add_argument('-o',
                        '--outdir',
                        help='output directory (will be passed to args.script with -o argument)',
                        required=True,
                        type=str)
    return parser.parse_args()

def read_files(datadir):
    temp = []
    for file in glob.glob(datadir):
        temp.append(pd.read_csv(file, index_col=False))
        
    SEED = file.split('_')[1]
    data = pd.concat(temp, axis=0, ignore_index=True)
    
    return data, SEED

def SA_dist_T(data, T, out):
    # Distribution of # ants by sensing area at T = T
    plt.figure(figsize = (8,6))
    dist_sensing_areaT = data[data['t'] == T]
    #dist_sensing_areaT = data[data['t'] == max(data['t'])]
    plt.hist(dist_sensing_areaT[' A'], density = True)
    plt.title('Distribution of Ant Survival by Sensing Area at T = '+str(T))
    plt.xlabel('Sensing Area')
    plt.ylabel('Frequency')
    plt.xlim(0,max(data[' A']))
    plt.savefig(out+'dist_sensing_area'+str(T)+'.png')
    plt.close()


def SA_timeseries(data, out):
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
    plt.savefig(out+'frequency_timeseries.png')
    plt.close()


def fitness_SA_timeseries(data, out):
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
    plt.savefig(out+'fitness_timeseries.png')
    plt.close()


def fitness_SA_scatter(data, out):
    # Distribution of average fitness by sensing area group
    plt.figure(figsize = (8,6))
    dist_fitnessT = data[data['t'] == max(data['t'])].groupby(' A').mean().reset_index()
    plt.scatter(dist_fitnessT[' A'], dist_fitnessT[' fitness'])
    plt.title('Average Fitness by Sensing Area at T = T')
    plt.xlabel('Sensing Area')
    plt.ylabel('Average Fitness')
    plt.xlim(0,max(data[' A']))
    plt.ylim(0,max(data[' fitness']))
    plt.savefig(out+'dist_fitnessT.png')
    plt.close()


def violin_fitness(data, out):
    # Violin plot of each sensing areas fitness distribution
    fig = plt.figure()
    fig, axes = plt.subplots(figsize = (8,6))
    sns.violinplot(' A',' fitness', data=data, ax = axes)
    axes.set_title('Distribution of Fitness by Sensing Area')
    #axes.yaxis.grid(True)
    axes.set_xlabel('Sensing Area')
    axes.set_ylim(0)
    axes.set_ylabel('Fitness')
    
    plt.savefig(out+'violin_fitness.png')
    plt.close()

def main():
    
    args = make_args()
    
    datadir = args.inputdir #csv/SEED_123*.csv
    outputdir = args.outdir
    
    data, SEED = read_files(datadir)
    out = outputdir+'SEED_'+str(SEED)+'_'
    
    SA_dist_T(data, 0, out)
    SA_dist_T(data, max(data['timestep']), out)
    SA_timeseries(data, out)
    fitness_SA_timeseries(data, out)
    fitness_SA_scatter(data, out)
    violin_fitness(data, out)
    

if __name__=="__main__":
    main()
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
    datalist = []
    for file in glob.glob(datadir):
        temp = pd.read_csv(file, index_col=False)
        seed = file.split('_')[1]
        gen = int(file.split('_')[3])
        seedtemp = [seed] * len(temp)
        gentemp = [gen] * len(temp)
        temp['seed'] = seedtemp
        temp['gen'] = gentemp
        datalist.append(temp)
        
    data = pd.concat(datalist, axis=0, ignore_index=True)
    
    return data



#def SA_dist_T(data, T, out):
#    # Distribution of # ants by sensing area at T = T
#    data = data[data['deadFlag'] == False]
#    plt.figure(figsize = (8,6))
#    dist_sensing_areaT = data[data['timestep'] == T]
#    #dist_sensing_areaT = data[data['t'] == max(data['t'])]
#    plt.hist(dist_sensing_areaT['A'], density = True)
#    plt.title('Distribution of Ant Survival by Sensing Area at T = '+str(T))
#    plt.xlabel('Sensing Area')
#    plt.ylabel('Frequency')
#    plt.xlim(0,max(data['A']))
#    plt.savefig(out+'dist_sensing_area'+str(T)+'.png')
#    plt.close()


#
#def SA_timeseries(data, out):
#    # Timeseries of # of ants, each line is a sensing area group
#    n = len(data['A'].unique())
#    colors = pl.cm.jet(np.linspace(0,1,n))
#    i = 0
#    plt.figure(figsize = (8,6))
#    data = data[data['deadFlag'] == False]
#    for A in data['A'].unique():
#        sensing_area_timeseries = data[data['A'] == A].groupby('timestep').count().reset_index()
#        plt.plot(sensing_area_timeseries['timestep'], sensing_area_timeseries['A'], color = colors[i])
#        i += 1
#    
#    plt.title('Timeseries for Ant Survival by Sensing Area')
#    plt.xlabel('Timesteps')
#    plt.ylabel('Frequency')
#    plt.xlim(0,max(data['timestep']))
#    plt.savefig(out+'frequency_timeseries.png')
#    plt.close()
    
    
    
def SA_gen_timeseries(data, out):
    # Timeseries of # of ants, each line is a sensing area group
    n = len(data['A'].unique())
    colors = pl.cm.jet(np.linspace(0,1,n))
    i = 0
    plt.figure(figsize = (8,6))
    data = data[data['deadFlag'] == False]
    for A in sorted(data['A'].unique()):
        sensing_area_timeseries = data[data['A'] == A].groupby('gen').count().reset_index()
        plt.plot(sensing_area_timeseries['gen'], sensing_area_timeseries['A'], color = colors[i], label = A)
        i += 1
    plt.legend()
    plt.title('Timeseries for Ant Survival by Sensing Area')
    plt.xticks(range(0, max(data['gen']), 20))
    plt.xlabel('Generation')
    plt.ylabel('Count')
    plt.xlim(0,max(data['gen']))
    plt.savefig(out+'gen_frequency_timeseries.png')
    plt.close()



#def fitness_SA_timeseries(data, out):
#    # Timeseries of average fitness, each line is a sensing area group
#    data = data[data['deadFlag'] == False]
#    n = len(data['A'].unique())
#    colors = pl.cm.jet(np.linspace(0,1,n))
#    i = 0
#    plt.figure(figsize = (8,6))
#    for A in sorted(data['A'].unique()):
#        fitness_timeseries = data[data['A'] == A].groupby('timestep').mean().reset_index()
#        plt.plot(fitness_timeseries['timestep'], fitness_timeseries['fitness'], color = colors[i], label = A)
#        i += 1
#    plt.legend()
#    plt.title('Timeseries for Average Fitness by Sensing Area')
#    plt.xlabel('Timesteps')
#    plt.ylabel('Average Fitness')
#    plt.xlim(0,max(data['timestep']))
#    plt.ylim(0,max(data['fitness']))
#    plt.savefig(out+'fitness_timeseries.png')
#    plt.close()
    
    
    
def fitness_SA_gen_timeseries(data, out):
    # Timeseries of average fitness, each line is a sensing area group
    data = data[data['deadFlag'] == False]
    n = len(data['A'].unique())
    colors = pl.cm.jet(np.linspace(0,1,n))
    i = 0
    plt.figure(figsize = (8,6))
    for A in sorted(data['A'].unique()):
        fitness_timeseries = data[data['A'] == A].groupby('gen').mean().reset_index()
        plt.plot(fitness_timeseries['gen'], fitness_timeseries['fitness'], color = colors[i], label = A)
        i += 1
    plt.legend()
    plt.title('Timeseries for Average Fitness by Sensing Area')
    plt.xlabel('Generation')
    plt.xticks(range(0, max(data['gen']), 20))
    plt.ylabel('Average Fitness')
    plt.xlim(0,max(data['gen']))
    plt.ylim(0,max(data['fitness']))
    plt.savefig(out+'seed_fitness_timeseries.png')
    plt.close()



#def fitness_SA_scatter(data, out):
#    data = data[data['deadFlag'] == False]
#    # Distribution of average fitness by sensing area group
#    plt.figure(figsize = (8,6))
#    dist_fitnessT = data[data['timestep'] == max(data['timestep'])].groupby('A').mean().reset_index()
#    plt.scatter(dist_fitnessT['A'], dist_fitnessT['fitness'])
#    plt.title('Average Fitness by Sensing Area at T = T')
#    plt.xlabel('Sensing Area')
#    plt.ylabel('Average Fitness')
#    plt.xlim(0,max(data['A']))
#    plt.ylim(0,max(data['fitness']))
#    plt.savefig(out+'dist_fitnessT.png')
#    plt.close()
    

#def maxfitness_SA_scatter(data, out):
#    # Distribution of average fitness by sensing area group
#    data = data[data['deadFlag'] == False]
#    plt.figure(figsize = (8,6))
#    dist_fitnessT = data[data['timestep'] == max(data['timestep'])].groupby('A').max().reset_index()
#    plt.scatter(dist_fitnessT['A'], dist_fitnessT['fitness'])
#    plt.title('Max Fitness by Sensing Area at T = T')
#    plt.xlabel('Sensing Area')
#    plt.ylabel('Max Fitness')
#    plt.xlim(0,max(data['A']))
#    plt.ylim(0,max(data['fitness']))
#    plt.savefig(out+'dist_maxfitnessT.png')
#    plt.close()


def violin_fitness(data, out, minSA, maxSA):
    # Violin plot of each sensing areas fitness distribution
    sns.set(font_scale=1.7)
    data = data[data['deadFlag'] == False]
    filtered_data = data[data['A'] >= minSA]
    filtered_data = filtered_data[filtered_data['A'] <= maxSA]
    fig = plt.figure()
    fig, axes = plt.subplots(figsize = (12,6))
    filtered_data['fitness'] = filtered_data['fitness']
    sns.violinplot('A','fitness', data=filtered_data, ax = axes, width=1.2)
    axes.set_title('Distribution of Fitness by Sensing Area')
    #axes.yaxis.grid(True)
    axes.set_xlabel('Sensing Area')
#    axes.set_yticks(np.arange(0,max(data['fitness']),0.2))
    axes.set_ylim(0,max(data['fitness']))
    axes.set_ylabel('Fitness')
    
    plt.savefig(out+str(maxSA)+'_violin_fitness.png')
    plt.close()


#def fitness_by_seed(data, out):
#    data = data[data['deadFlag'] == False]
#    fitness_by_seed = data.groupby('seed').mean().reset_index()
#    plt.scatter(fitness_by_seed['fitness'],fitness_by_seed['seed'])
#    plt.title('Average Fitness per Generation')
#    plt.xlabel('Sensing Area')
#    plt.ylabel('Max Fitness')
#    plt.xlim(0,max(data['A']))
#    plt.ylim(0,max(data['fitness']))
#    plt.savefig(out+'seed_dist_maxfitnessT.png')
#    plt.close()

    
def main():
    
    # pyhton3 plots.py -i DIRECTORYNAME -o figs/
    
    args = make_args()
    
    datadir = args.inputdir
    out = args.outdir
    
    data = read_files(datadir)

#    out = outputdir+'SEED_'+str(SEED)+'_'
#    out = outputdir+'_TEST_'
    
    violin_fitness(data, out, 1, 5)
    violin_fitness(data, out, 6, 10)
    fitness_SA_gen_timeseries(data, out)
    SA_gen_timeseries(data, out)

    

if __name__=="__main__":
    main()
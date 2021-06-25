#!/usr/bin/env python3

import os
import pandas as pd
import scipy.interpolate
import outilsLecture as olec
import outilsDivers as odiv
import sys

# postProcess folder
cwd = 'postProcessing/line'
if os.listdir(cwd) != []:
    print("Lecture des fichiers dans {}".format(cwd))
    all_folders = os.listdir(cwd)
else:
    raise ValueError('{} is empty'.format(cwd))

# get time vector
print("Création du vecteur temporel")
time_vec = sorted([float(i) for i in all_folders])

#Read output file option
outputFile = olec.readFileOption(sys.argv, ["-output","--output",
                                            "-outputFile","--outputFile"],
                                 default = "line_probes.csv",
                                 extension = "csv")

#Read time range options
tmin = olec.readValueOption(sys.argv, ['-tmin', '--tmin'], default = time_vec[0])
tmax = olec.readValueOption(sys.argv, ['-tmax', '--tmax'], default = time_vec[-1])

#Only keep given time range
print("Intervalle de temps : [{},{}]".format(tmin,tmax))
tminIndex = odiv.find(time_vec, tmin, default = 0)
tmaxIndex = odiv.find(time_vec, tmax, default = None)
print("index [{},{}]".format(tminIndex,tmaxIndex))
time_vec = time_vec[tminIndex:tmaxIndex]

for idx, time in enumerate(time_vec):
    if str(time).split(".")[-1] == "0":
        all_folders[idx] = str(time).split(".")[0]
    else:
        all_folders[idx] = str(time)

all_folders = all_folders[tminIndex:tmaxIndex]
total_time_steps = len(time_vec)

# get names of the probes
lines = []
for filename in os.listdir(os.path.join(cwd, all_folders[0])):
    if filename.endswith('alpha.water.xy'):
        lines.append(filename.split('_')[0])
if lines == []:
    raise ValueError('expected *alpha_water.xy files, found none')

# initialize data frame
df = pd.DataFrame(index=time_vec, columns=lines)

#Sort dataframe to get probes in order (if numbered)
df.sort_index(axis=1, inplace = True)  

# extract interface at each time step for all line probes
print('extracting alpha values for every line probe...')
for br, folder in enumerate(all_folders, 1):
    
    print('time step: {} s, ({}/{})'.format(folder, br, total_time_steps))
    folder_path = os.path.join(cwd, folder)
    
    for filename in os.listdir(folder_path):

        probename = filename.split('_')[0]
        alpha_water = pd.read_csv(os.path.join(folder_path, filename),
                                      header=0, delimiter='\t')
        depth = alpha_water.iloc[:, 0]
        alpha = alpha_water.iloc[:, 1]
        f = scipy.interpolate.interp1d(alpha, depth)
        interface = f(0.5).item()
        df.at[float(folder), probename] = interface
print('done.')

# normalize the results
df -= df.iloc[0, 0]

# save results
print('saving results to {}'.format(outputFile))
df.to_csv(outputFile, sep=',', index_label='time')

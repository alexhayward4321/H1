#%% 
import numpy as np
import pandas as pd
import csv

import re

# Bit messy, but loads in the neutron and gamma energy bin information

path = "/Users/user1/Documents/Summer Internship 2022/Python code/openmc/H1/data/archive/neutron_bins.txt"
with open(path) as f:
    data = f.read() + ' '

neutron_bins = []
word = ''
for c in data:
    if c in [' ', '\n']:
        neutron_bins.append(float(word))
        word = ''
    else:
        word += c

neutron_bins = np.array(neutron_bins)

gamma_bins = np.array([1.0e3, 1.0e4, 2.0e4, 3e4, 4.5e4, 6e4, 7e4,
7.5e4, 1e5, 1.5e5, 2e5, 3e5, 4e5, 4.5e5, 5.1e5, 5.12e5, 6e5, 7e5, 8e5, 1e6, 1.33e6,
1.34e6, 1.5e6, 1.66e6, 2e6, 2.5e6, 3e6, 3.5e6, 4e6, 4.5e6, 5e6, 5.5e6, 6e6, 6.5e6, 7e6,
7.5e6, 8e6, 1e7, 1.2e7, 1.4e7, 2e7, 3e7, 5e7])


def read_partisn_out(filepath):
    '''
    Reads partisn output file to extract quantity for each group

    Parameters:
        filepath (str): file path to partisn output file
    
    Returns:
        pd.DataFrame with 
    '''
    with open(filepath) as f:
        lines = f.readlines()
    data_lines = []
    labels = []
    for i, line in enumerate(lines):
        match = re.search(r'. sum .', line)
        if match:
            refined = line[match.end()-1:-1] + ' '
            data_lines.append(refined)
            defined = re.sub(r'[*\n]', '', lines[i-5])
            redefined = re.sub('zone', '', defined) + ' '
            labels.append(redefined)
    data_lines = data_lines[1:]
    labels = labels[1:]
    
    nums = []
    for line in data_lines:
        space_hist = True
        num = ''
        for c in line:
            if c == ' ' and space_hist:
                continue
            elif c == ' ' and not space_hist:
                space_hist = True
                nums.append(num)
                num = ''
            else:
                num += c
                space_hist = False

    words = []
    for line in labels:
        space_hist = True
        num = ''
        for c in line:
            if c == ' ' and space_hist:
                continue
            elif c == ' ' and not space_hist:
                space_hist = True
                words.append(num)
                num = ''
            else:
                num += c
                space_hist = False
    
    labels = pd.Series(words)
    nums = pd.Series(nums, dtype=np.float64)
    df = pd.concat([labels, nums], axis=1)
    df.set_index(0, inplace=True)
    df.rename_axis(index='group', inplace=True)
    return df


def read_neutron_flux(filename, reverse=False):
    with open(filename) as f:
        text = f.readlines()
        numbers = []
        if reverse:
            for line in text:
                space_count = 0
                for i, c in enumerate(line):
                    if c == ' ':
                        space_count += 1
                    if space_count == 5:
                        numbers.append(line[i+1:].replace('\n', ''))
                        space_count = 0
                        continue
            array = np.array(numbers, dtype=np.float64)
            gammas = array[:len(gamma_bins)-1]
            neutrons = array[len(gamma_bins)-1:]
        else:
            for line in text:
                space_count = 0
                for i, c in enumerate(line):
                    if c == ' ':
                        space_count += 1
                    if space_count == 3:
                        numbers.append(line[i+1:].replace('\n', ''))
                        space_count = 0
                        continue
            array = np.array(numbers, dtype=np.float64)
            neutrons = np.flip(array[:len(neutron_bins)-1])
            gammas = np.flip(array[len(neutron_bins)-1:])
    return neutrons, gammas
                


if __name__=='__main__':
    # filename = '/Users/user1/Downloads/High energy neutron source/partisn-14mev_100i.OUT'
    # out_partisn = read_partisn_out(filename)
    # print(out_partisn)
    filename = '/Users/user1/Documents/Summer Internship 2022/Python code/data/partisn/high_energy/neutron_flux.txt'
    neutron_flux, gamma_flux = read_neutron_flux(filename)

    
    
# %%

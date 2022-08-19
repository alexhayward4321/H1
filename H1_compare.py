#%%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openmc

from importlib import reload
import os
import sys
sys.path.append('/Users/user1/Documents/Summer Internship 2022/Python code/openmc/H1')

import utils.plotting as p
from utils.data_load import read_partisn_out, neutron_bins, gamma_bins, read_neutron_flux

reload(p)

n=3
N=7

##############
def compare(n, N):
    # Reading in data
    print('remember to undo this')

# Reading in data

# Reading deterministic data directly from PARTISN output file
filenames = ['', '/Users/user1/Documents/Summer Internship 2022/Python code/openmc/H1/data/partisn/thermal/partisn3.OUT',
            '/Users/user1/Documents/Summer Internship 2022/Python code/openmc/H1/data/partisn/high_energy/partisn-14mev_100i.OUT']
df = read_partisn_out(filenames[n-1])
df_refined = df[df.index != 'volume']
df_t = df_refined.T
overall_neutron_flux = df_t.pop('neut')
overall_gamma_flux = df_t.pop('gama')
if n == 3:
    nth = df_t.pop('nth')
det_g1 = np.flip(df_t.T.iloc[:, 0].values)

# ADJUSTING DET TO ACCOUNT FOR STRANGE BIN STRUCTURE INCOHERENCE
det_g1 = det_g1[1:]
det_g1_bins = gamma_bins[:len(det_g1)+1]

# Reading in alternative deterministic data
filename = '/Users/user1/Documents/Summer Internship 2022/Python code/openmc/H1/data/partisn/high_energy/fluxes2.txt'
det_n, det_g = read_neutron_flux(filename, reverse=True)


# Reading gamma MC data
openmc_gamma_data = pd.read_csv(f'data/processed/output_{n}g_e{N}.csv')
stat_g = openmc_gamma_data['fg'].values
stat_g1 = stat_g[:len(det_g1)]
# Reading neutron MC data
neutron_data = pd.read_csv(f'data/processed/output_{n}n_e{N}.csv')
stat_n = neutron_data['fn'].values


# Defining various useful energy bin values

bin_mean_g1 = (det_g1_bins[1:] + det_g1_bins[:-1])/2
diff_g1 = det_g1_bins[1:] - det_g1_bins[:-1]
leth_g1 = np.log(det_g1_bins[1:] / det_g1_bins[:-1])

bin_mean_g = (gamma_bins[1:] + gamma_bins[:-1])/2
diff_g = gamma_bins[1:] - gamma_bins[:-1]

bin_mean_n = (neutron_bins[1:] + neutron_bins[:-1]) / 2
diff_n = (neutron_bins[1:] - neutron_bins[:-1]) / 2

# %% ###########################
# Comparing openmc vs partisn gammas


p.plot_log_axes(bin_mean_g1, [det_g1, stat_g1],
                n, N, 'gamma_flux', legend=['det_g1', 'stat_g1'])
p.plot_log_axes(bin_mean_g1, [det_g1/diff_g1, stat_g1/diff_g1],
                n, N, 'gamma_flux_diff', legend=['det_g1', 'stat_g1'])
p.plot_log_axes(bin_mean_g1, [det_g1/leth_g1, stat_g1/leth_g1],
                n, N, 'gamma_flux_leth', legend=['det_g1', 'stat_g1'])


# stat_det_g_fact = 4 * np.pi * 0.52**2
stat_det_g_fact = 4.5
lead = 6
try:
    stat_det_g_fact = (stat_g1[lead:] / det_g1[lead:])[:-1].mean()
except Exception:
    print(det_g1)
p.plot_log_axes(bin_mean_g1, [det_g1, stat_g1/stat_det_g_fact], 'Flux',
                n, 'g', N, legend=['det_g1', 'stat_g1'])

# close up
fig, ax = plt.subplots()
ax.plot(bin_mean_g1, det_g1, bin_mean_g1, stat_g1/stat_det_g_fact)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Energy')
ax.set_ylabel('Flux')
ax.set_xlim(1e5, 1.5e6)
ax.set_ylim(5e-5, 5e-3)


#%%
# Comparing other data
# Plotting gamma and neutron fluxes
p.plot_log_axes(bin_mean_g, [det_g, stat_g],
                n, N, 'gamma_2', legend=['det_g', 'stat_g1'])
p.plot_log_axes(bin_mean_n, [det_n, stat_n],
                n, N, 'neutron_2', legend=['det_g', 'stat_g1'])


# Generating and plotting factored graphs

# gamma
lead = 6
lag = -6
fact_g = (stat_g[lead:lag] / det_g[lead:lag]).mean()
p.plot_log_axes(bin_mean_g, [det_g, stat_g/fact_g],
                n, N, 'filename', legend=['det_g', 'stat_g1'], savefig=False)

# neutron
lead = 6
lag = -6
numerator = stat_n[lead:lag][stat_n[lead:lag] != 0]
denominator = det_n[lead:lag][stat_n[lead:lag] != 0]
fact_n = (numerator / denominator).mean()
p.plot_log_axes(bin_mean_n, [det_n, stat_n/fact_n],
                n, N, 'filename', legend=['det_g', 'stat_g1'], savefig=False)

kfk_fact = 3442
p.plot_log_axes(bin_mean_n, [det_n, stat_n/kfk_fact],
                n, N, 'filename', legend=['det_g', 'stat_g1'], savefig=False)



if __name__ == '__main__':
    n = 3
    N = 6
    compare(n, N)

# %%

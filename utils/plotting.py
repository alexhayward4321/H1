#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os

def plot_log_axes(x, y, n, N, filename, xlabel='Energy [eV]', ylabel='Flux',
                  legend=None, dir='', savefig=True, other=False):
    """
    Plots x against (multiple) y('s) and saves result to an image file.

    Parameters:
        x (np.array) : x axis values
        y (np.array, list of ndarrays): y axis values
        xlabel (str): x axis label
        ylabels (str): y axis label
        labels (str): labels for each dependent variable
        n (int): model source energy reference number
        particle (str): particle the plot is describing
        dir (str): optional directory to save images to

    Returns:
        N/A. Saves graph to image file.
    """
    
    # Graphing
    fig, ax = plt.subplots()

    if type(y) == list:
        for i in range(len(y)):
            ax.plot(x, y[i])
    else:
        ax.plot(x, y)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(legend)

    # Saving plots to files
    if not savefig:
        return
    # Saving file
    energy = 'high_energy/' if n==3 else 'thermal/'
    subdir = 'comparison' if type(y) is list else 'single'
    # Making folders if they don't exist
    dir= os.path.join('graphs/', energy, f'e{N}/', subdir)
    if not os.path.exists(dir):
        os.mkdir(dir)
    filepath = os.path.join(dir, filename)
    plt.savefig(filepath, dpi=500)


def plot_bar_log_axes(x, y, width, ylabel, n, particle, xlabel='Energy [eV]', dir=''):
    fig, ax = plt.subplots()
    ax.bar(x, y, width=width, log=True, align='edge')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Saving graph
    if len(dir) > 0:
        dir = dir + '/'
    plt.savefig(f"{dir}single/{ylabel}_{n}{particle}h", dpi=1000)


# Testing
if __name__ == "__main__":
    print('Testing ...')
# %%

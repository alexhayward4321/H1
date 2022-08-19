#%%

# Some python typesetting functions for Ivo to quickly and easily produce output

import numpy as np
import pandas as pd
import re

from sqlalchemy import true

# number to string formatter for rsfnam. Looks like you can use basically any string
# format. Might exist a rule that can't begin with a number. Otherwise, should just
# be able to use scientific notation. Let's start it with a g for 'convention'.
# We will also have '.' as 'p'

def rsfnam(array):
    '''
    Input: array of floats
    -----------
    Output: array of rsfnam arbitrarily defined string formats
    '''
    out = []
    for n in array:
        it = -1
        while n >= 1:
            it+=1
            n = n/10
        n *= 10
        num = f'g{n.round(4)}e{it}'.replace('.', 'p')
        out.append(num)
    out = ' '.join(out)
    return out


def rsfe(n_start, n_end):
    len = n_end - n_start + 1
    out = []
    for i in range(len):
        string = f'{n_start+i}z 16z 1 f0;'
        out.append(string)
    out = ' '.join(out)
    return out

# Extracts group data from partisn and puts it in a dataframe


if __name__ == '__main__':

    from data_load import neutron_bins
    # Testing

    out_rsfnam = rsfnam(neutron_bins)
    out_rsfe = rsfe(211, 236)



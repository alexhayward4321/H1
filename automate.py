#%%
import os

import H1_run
from H1_compare import compare


n_list = [2,3]
N_list = range(8,10)

for n in n_list:
    for N in N_list:
        H1_run.main(n, N)
        H1_run.post_processing(n, N)
        compare(n, N)
        
# %%

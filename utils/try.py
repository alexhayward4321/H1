#%%
import binascii

with open('/Users/user1/Downloads/High energy neutron source/rzmflx', 'rb') as f:
    data = f.read(45)
    data1 = binascii.b2a_uu(data)

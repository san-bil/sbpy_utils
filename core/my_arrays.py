import numpy as np
import copy

def cell2mat(input_arg,axis,use_copy=True):
    curr=input_arg[0]
    
    if(len(input_arg)>1):
        for f in range(1,len(input_arg)):
            curr = np.concatenate((curr,input_arg[f]),axis)
    
    if use_copy:
        curr=copy.deepcopy(curr)
    return curr


def my_concatenate(input_arg,axis,newaxis_idx=0):
    
    ndims=[x.ndim for x in input_arg]
    max_ndim=np.max(ndims)
    input_arg2=[x if x.ndim==max_ndim else np.expand_dims(x, newaxis_idx) for x in input_arg]
    
    return np.concatenate(tuple(input_arg2),axis)

def test_cell2mat():
    x=cell2mat([np.arange(0,9).reshape(3,3),2*np.arange(0,9).reshape(3,3)],1)
    print(x)
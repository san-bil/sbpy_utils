import numpy as np
from numpy import ravel_multi_index,unravel_index
from numba import jit

def sub2ind(subs):
    return ravel_multi_index(subs)

def ind2sub():
    raise NotImplementedError()



@jit('double[:, :](double[:, :], double[:, :])', cache=True)
def ragged_slice_4_jit(A, B):
    C = np.zeros(B.shape)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            for k in range(A.shape[2]):
                C[i, j, k] = A[i, j, k, B[i, j, k]]
    return C


def ragged_slice_4(A,B):
    assert(A.ndim==4 and B.ndim==4)
    if(A.shape[3]==1):
        C=A
    else:
        C=np.zeros(B.shape)
        for i in range(0,A.shape[0]):
            for j in range(0,A.shape[1]):
                for k in range(0,A.shape[2]):
                        C[i,j,k,0] = A[i,j,k,B[i,j,k,0]]
    return C


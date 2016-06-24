import numpy as np
import itertools
import copy
from collections import OrderedDict

def xcov_matrix(x,y):
    return np.dot(np.transpose(x-np.mean(x,0)),(y-np.mean(y,0))) / (x.shape[0]-1)
    

def test_xcov_matrix():
    mydict={}
    mydict['x']=np.random.uniform(0,1,(100,8))
    mydict['y']=np.random.uniform(0,1,(100,8))
    import scipy.io
    mydict['xcov_res']=xcov_matrix(mydict['x'], mydict['y'])
    scipy.io.savemat('/Users/sanjay/xcov_matrix_test.mat', mydict)
    
def corrcoef_matrix(X,Y):

    out = np.zeros((X.shape[1],Y.shape[1]))
        
    for comb in itertools.product(range(0,X.shape[1]),range(0,Y.shape[1])):
        tmp=np.corrcoef(X[:,comb[0]],Y[:,comb[1]]);
        out[comb[0],comb[1]] = tmp[0,1];
    return out

def test_corrcoef_matrix():
    mydict={}
    mydict['x']=np.random.uniform(0,1,(20,3))
    mydict['y']=np.random.uniform(0,1,(20,3))
    import scipy.io
    mydict['corrcoef_res']=corrcoef_matrix(mydict['x'], mydict['y'])
    mydict['np_corrcoef_res']=np.corrcoef(mydict['x'], mydict['y'])
    scipy.io.savemat('/Users/sanjay/corrcoef_matrix_test.mat', mydict)
    


def find_top_correlations_greedy(corr_matrix,num_corrs=0):
    
    
    if num_corrs==0:
        num_corrs=np.min(corr_matrix.shape); 
    working_corr_matrix=copy.deepcopy(corr_matrix)
    corrs=[];
    corrs=OrderedDict()
    ctr=0;
    while(1):
    
        col_corr_maxes=np.max(working_corr_matrix,0)
        col_corr_argmaxes=np.argmax(working_corr_matrix,0)
        
        max_corr = np.max(col_corr_maxes);
        max_corr_col_idx=np.argmax(col_corr_maxes)
        
        max_corr_row_idx=col_corr_argmaxes[max_corr_col_idx]
            
        corrs[(max_corr_row_idx,max_corr_col_idx)]=max_corr;
    
        working_corr_matrix[max_corr_row_idx,:]=-np.inf
        working_corr_matrix[:,max_corr_col_idx]=-np.inf
        ctr=ctr+1;
    
        if(ctr==num_corrs):
            break;

    return corrs

def test_find_top_correlations_greedy():
    dummy_corr_matrix=np.random.uniform(0,1,(5,5))*10;
    print(dummy_corr_matrix)
    print(find_top_correlations_greedy(dummy_corr_matrix,4))

#test_find_top_correlations_greedy()
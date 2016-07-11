import numpy as np

def get_normalized_laplacian(adjacency_matrix):
    
    degree=np.sum(adjacency_matrix,1)
    
    d_inv_half=np.divide(np.ones(degree.shape),np.sqrt(degree));
    
    out = np.eye(adjacency_matrix.shape)-np.dot(np.diag(d_inv_half)*np.dot(adjacency_matrix*np.diag(d_inv_half)))
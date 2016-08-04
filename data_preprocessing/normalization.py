import numpy as np


def unit_denormalize_labels(label_col, real_range):
    return shift_array_min_max(label_col, real_range, [0, 1])
    
def shift_array_min_max(array,new_bounds,real_range=None):
    array=np.asarray(array)
    if real_range is None:
        empirical_min = np.min(array);
        empirical_max = np.max(array);
    else:
        empirical_min = real_range[0];
        empirical_max = real_range[1];
    
    empirical_range = empirical_max-empirical_min;
    
    desired_range = np.diff(new_bounds);
    
    new_array=array-empirical_min;
    new_array=new_array*desired_range/empirical_range;
    new_array=new_array+new_bounds[0];
    return new_array

    
def test_shift_array_min_max():
    print([ f for f in shift_array_min_max(np.asarray(map(float,[0,1,2,3,4,5,6,7,8])),[0,1],[0,8])])
    

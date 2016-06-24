import sys,os
import numpy as np
from os.path import dirname as dirname
sys.path.append(dirname(dirname(os.path.realpath(__file__))))
from sbpy_utils.core.sets import my_unique
from sbpy_utils.data_preprocessing.normalization import shift_array_min_max

def unit_normalize_labels(label_col,real_range):

    return shift_array_min_max(label_col,[0, 1],real_range)

def convert_labels_to_one_hot(label_col,num_classes=-1,class_lower_bound=-1):
    
    labels = sorted(my_unique(label_col))
    
    if num_classes==-1 :
        num_classes=len(labels)
        
    if class_lower_bound==-1:
        class_lower_bound=np.min(labels)
    
    
    if(True or np.min(labels)<=0 or class_lower_bound<=0):
        label_col = [x-class_lower_bound for x in label_col]
        labels = [x-class_lower_bound for x in labels]
    
        
    label_matrix = np.zeros((len(label_col),num_classes));
    for i in range(0,len(labels)):
        iv=[ x==labels[i] for x in label_col]
        index_vec=np.nonzero(iv)[0].astype(int)
        label_matrix[index_vec.astype(int),(labels[i]*np.ones(index_vec.shape)).astype(int)]=1 
    return label_matrix


def convert_labels_to_one_hot_w_neutral(orig_label_col,num_classes,class_lower_bound,neutral_class):

    label_col=orig_label_col;
    labels = my_unique(label_col)
    
    if(not 'num_classes' in locals()):
        num_classes=len(labels)
    if(not 'class_lower_bound' in locals()):
        class_lower_bound=min(labels)
    if(not 'neutral_class' in locals()):
        neutral_class=0
    
    neutral_locations=[tmp==neutral_class for tmp in label_col]    
    
    if(True or min(labels)<=0):
        label_col=[tmp-class_lower_bound for tmp in label_col]
        labels = [tmp-class_lower_bound for tmp in labels if (not tmp==neutral_class)]
        
    label_matrix = np.zeros((len(label_col),num_classes))
    
    for i in range(0,len(labels)):
        iv=[ x==labels[i] and (not neutral_locations[j]) for j,x in enumerate(label_col)]
        index_vec=np.nonzero(iv)[0].astype(int)
        label_matrix[index_vec.astype(int),labels[i]*np.ones(index_vec.shape).astype(int)]=1 
       
    return label_matrix
    

def integer_to_one_hot( integer_vector, n_labels=-1 ):
    
    if(isinstance(integer_vector, list)):
        integer_vector=np.asarray(integer_vector)
    
    if(n_labels==-1):
        n_labels=np.max(integer_vector)+1
    
    return np.eye(n_labels)[integer_vector][:,1:]

def one_hot_to_integer( one_hot_matrix ):
    
    one_ts = np.argmax(one_hot_matrix,1)+1;

    return one_ts * map(lambda x:float(x),np.sum(one_hot_matrix,1) > 0);

def test_integer_to_one_hot():
    integer_vector=[1, 1, 2, 1, 4, 0, 3, 1];
    print(integer_to_one_hot(integer_vector,10))


def test_one_hot_to_integer():
    one_hot_matrix = np.asarray([[0,1,0],
                                 [1,0,0],
                                 [0,1,0],
                                 [0,0,1]])
    print one_hot_to_integer(one_hot_matrix)


def test_all():
    pass
    #test_one_hot_to_integer()
    #test_integer_to_one_hot()
    
    
import numpy as np
import copy

def list_traverse_apply(o, callback, tree_types=list):
    if isinstance(o, tree_types):
        return [list_traverse_apply(tmp, callback, tree_types) for tmp in o]
    else:
        return callback(o)
    
    
def list_split(in_list,idxs):
    idx_chunks=np.split(np.arange(len(in_list)),idxs)
    list_splits = [[in_list[tmp2] for tmp2 in tmp] for tmp in idx_chunks]
    return list_splits

#def test_list_split():
    #mylist=['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']
    #print(list_split(mylist,[5]))
#test_list_split()

        
#def test_traverse():
    #import pprint
    #tmp=[[1],[2,3,4,[5]],[[6]]]
    #pprint.pprint(tmp)
    #new_tmp=traverse(tmp, lambda x:x+1, tree_types=list)
    #pprint.pprint(new_tmp)
    
#test_traverse()
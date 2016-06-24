import itertools

def my_unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def test_my_unique():
    import numpy as np
    mylist=np.asarray([9,3,6,1,3,6,2])
    print(mylist)
    print(my_unique(mylist))
    
def my_sort(alist):
    return (sorted(alist), sorted(range(len(alist)), key=lambda k: alist[k]))

def my_intersect(list_1,list_2):
    ind_dict_1 = dict((k,i) for i,k in enumerate(list_1))
    ind_dict_2 = dict((k,i) for i,k in enumerate(list_2))
    inter = set(ind_dict_1).intersection(list_2)
    inter2 = set(ind_dict_2).intersection(list_1)

    indices_1 = [ ind_dict_1[x] for x in inter ]
    indices_2 = [ ind_dict_2[x] for x in inter2 ]
    return (inter,indices_1,indices_2)

def group_by(lists,get_key_callback):

    new_lists=[];
    running_keys = [];
    
    for i in range(1,len(lists)):
        keys = [get_key_callback(x) for x in lists[i]];
        sort_res=my_sort(keys);
        sorted_keys=sort_res[0]
        sort_order=sort_res[1]
        running_keys.append(set(sorted_keys));
    
    
    global_key_intersection = set.intersection(*running_keys);
    
    for i in range(0,len(lists)):
        keys = [get_key_callback(x) for x in lists[i]];
        sort_res=my_sort(keys);
        sorted_keys=sort_res[0]
        sort_order=sort_res[1]
        intersect_res = my_intersect(sorted_keys,global_key_intersection)
        IA=intersect_res[1]
        new_lists.append([lists[i][y] for y in [sort_order[x] for x in IA]]) ;
    
    lists_lengths = [len(x) for x in new_lists];
   
    assert(sum([x==lists_lengths[1] for x in lists_lengths])==length(lists_lengths));

def cartprod(*args):
    cartprod_res=[]
    for element in itertools.product(*args):
        cartprod_res.append(element)
    return cartprod_res


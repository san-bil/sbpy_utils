function [ kv_map ] = kv_sixr( keys,idxs,new_val,kv_map)

%kv_get + indexer

val=kv_get_recursive(keys,kv_map);

val(idxs{:})=new_val;

kv_map = kv_set_recurse(keys,val,kv_map);
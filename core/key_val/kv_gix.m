function [ idxd_val ] = kv_gixr( keys,idxs,kv_map)

val=kv_get_recursive(keys,kv_map);

idxd_val=val(idxs);
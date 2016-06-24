function [ idxd_val ] = kv_gixr( keys,idxs,kv_map)

%kv_get + indexer

val=kv_get_recursive(keys,kv_map);

idxd_val=val(idxs{:});
function out = kv_create_lists(keys)

out = [(force_col_vec(keys)) cellcell([length(keys),1],0) ];
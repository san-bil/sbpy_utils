function out = kv_create_from_keys(kvmap)

out = [(force_col_vec(kv_getkeys(kvmap))) cell(length(kvmap),1) ];
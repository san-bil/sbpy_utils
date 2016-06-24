function prefixed_kv_map = kv_prefix_all_vals(prefix, kv_map)

prefixer = @(some_str)[prefix some_str];

kv_vals = kv_map(:,2);

kv_vals_prefixed = cellfun(prefixer,kv_vals,'UniformOutput',0);


prefixed_kv_map = kv_map;
prefixed_kv_map(:,2)=kv_vals_prefixed;
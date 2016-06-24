function prefixed_kv_map = kv_prefix_all_keys(prefix, kv_map)

prefixer = @(some_str)[prefix some_str];

kv_keys = kv_map(:,1);

kv_keys_prefixed = cellfun(prefixer,kv_keys,'UniformOutput',0);


prefixed_kv_map = kv_map;
prefixed_kv_map(:,1)=kv_keys_prefixed;
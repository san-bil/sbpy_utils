function suffixed_kv_map = kv_suffix_all_keys(suffix, kv_map)

suffixer = @(some_str)[some_str suffix];

kv_keys = kv_map(:,1);

kv_keys_suffixed = cellfun(suffixer,kv_keys,'UniformOutput',0);


suffixed_kv_map = kv_map;
suffixed_kv_map(:,1)=kv_keys_suffixed;
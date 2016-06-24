function suffixed_kv_map = kv_suffix_all_vals(suffix, kv_map)

suffixer = @(some_str)[some_str suffix];

kv_vals = kv_map(:,2);

kv_vals_suffixed = cellfun(suffixer,kv_vals,'UniformOutput',0);


suffixed_kv_map = kv_map;
suffixed_kv_map(:,2)=kv_vals_suffixed;
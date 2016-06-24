function new_dict = kv_order_keys(ordered_keys, dict)

new_dict = {};
mutable_dict = dict;
for i=1:length(ordered_keys)

    okey = ordered_keys{i};
    new_dict = kv_set(okey,kv_get(okey,dict),new_dict);
    mutable_dict = kv_rm(okey,mutable_dict);
    
end

new_dict = kv_join(new_dict, mutable_dict);
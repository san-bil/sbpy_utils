function new_map = kv_append_val(key, append_val, map)

list = kv_get(key,map,{});
list{end+1}=append_val;
new_map = kv_set(key,list,map);

end
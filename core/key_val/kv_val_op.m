function new_map = kv_val_op(key, map,operator)

val = kv_get(key,map);
op_val = operator(val);    
new_map = kv_set(key,op_val,map);
    

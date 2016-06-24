function new_map = kv_allvals_op(map,operator)

keys=kv_getkeys(map);

new_map = {};
for i =1:length(keys)

    key = keys{i};
    val = kv_get(key,map);
    
%     if(iscell(val))
%         val = cell2mat(val);
%     end
    
    op_val = operator(val);    
    new_map = kv_set(key,op_val,new_map);
    
end
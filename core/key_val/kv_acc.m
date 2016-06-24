function [ acc ] = kv_acc( key, kv_maps )
%KV_ACC Summary of this function goes here
%   Detailed explanation goes here
acc = {};
for i = 1:length(kv_maps)
   
    acc{i} = kv_get(key,kv_maps{i});
    
end


end


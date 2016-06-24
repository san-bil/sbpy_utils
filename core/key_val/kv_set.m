function [ kv_map ] = kv_set( key, val, kv_map, col_idx )

% in: a string key, an associated value, a 2-column cell array representing a dictionary (first column==string keys, second column==values)
%
% out: the dictionary with either an extra key-value pair inserted, or the old value (corresponding to the key) overwritten
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

if(~exist('col_idx','var'))
    col_idx = 2;
end

my_flag=0;
for i=1:size(kv_map,1)
    if((ischar(kv_map{i,1}) && ischar(key) && strcmp(kv_map{i,1},key)) || (isnumeric(kv_map{i,1}) && isnumeric(key) && (kv_map{i,1}==key)))
        kv_map{i,col_idx} = val;
        my_flag = 1;
    end
end

if(my_flag==0)
%    warning(['adding key: ',key])
    kv_map = [kv_map;{key,val}];
end

end


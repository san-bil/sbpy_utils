function [ output_args,val ] = kv_rm( key,kv_map)


% in: a string key, a 2-column cell array representing a dictionary (first column==string keys, second column==values)
%
% out: the dictionary, with the input key (and corresponding value) removed
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

val =kv_get(key,kv_map);

my_flag = -1;
for i=1:size(kv_map,1)    
    if((ischar(kv_map{i,1}) && ischar(key) && strcmp(kv_map{i,1},key)) || (isnumeric(kv_map{i,1}) && isnumeric(key) && (kv_map{i,1}==key)))
        my_flag = i;
    end
end

if(my_flag>=0)
    output_args = [kv_map(1:my_flag-1,:); kv_map(my_flag+1:end,:)];
else
    output_args = kv_map;
end
end


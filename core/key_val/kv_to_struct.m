function struct = kv_to_struct( kv_map)

% in: a string key, a 2-column cell array representing a dictionary (first column==string keys, second column==values), 
% (optional) a default value to be returned if there is no matching key
%
% out: the associated value, or a default value is there is no matching key
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue



struct=[];
for i=1:size(kv_map,1)
    if(ischar(kv_map{i,1}))
        struct = setfield(struct,kv_map{i,1},kv_map{i,2});
    else
        warning('kv_to_struct(): cannot create struct field with non-string key')
    end
end
function kv_map = kv_from_struct( struct)

% in: a string key, a 2-column cell array representing a dictionary (first column==string keys, second column==values), 
% (optional) a default value to be returned if there is no matching key
%
% out: the associated value, or a default value is there is no matching key
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue



kv_map={};
keys = fieldnames(struct);
for i=1:length(keys)
    
    kv_map = kv_set(keys{i}, getfield(struct,keys{i}),kv_map);
end
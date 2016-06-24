function [matching_keys,matching_key_idxs] = kv_find(key_substr,dict)

keys = kv_getkeys(dict);
matching_key_idxs = find(cell2mat(cellfun(@(z)~isempty(findstr(z,key_substr)),keys,'UniformOutput',0)));
matching_keys = keys(matching_key_idxs);

if(length(matching_keys)==1)
    matching_keys = matching_keys{1};
end


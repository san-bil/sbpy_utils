function out = kv_filter(map_to_filter,keys,include_or_exclude)

in_map = {};
ex_map = {};

if(~exist('include_or_exclude','var'))
    include_or_exclude='include';
end

for i = 1:size(map_to_filter,1)
    
    if(ismember(map_to_filter{i,1},keys))
        in_map = [in_map; map_to_filter(i,:)];
    else
        ex_map = [ex_map; map_to_filter(i,:)];
    end
    
end

if(strcmp(include_or_exclude,'include'))
    out = in_map;
elseif(strcmp(include_or_exclude,'exclude'))
    out = ex_map;
else
    error('map filter error');
end
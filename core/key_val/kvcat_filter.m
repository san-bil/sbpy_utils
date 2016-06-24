function out = kvcat_filter(map_to_filter,categories,include_or_exclude)

in_map = {};
ex_map = {};

for i = 1:size(map_to_filter,1)
    is_is_category_set = ~isempty(intersect(strsplit(map_to_filter{i,3},','),strsplit(categories,',')));
    if(is_is_category_set)
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
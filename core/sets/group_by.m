function [new_lists] = group_by(lists,get_key_callback)

new_lists={};
running_keys = {};

for i = 1:length(lists)
    keys = (cellfun(get_key_callback,lists{i},'UniformOutput',0));
    [sorted_keys,sort_order]=sort((keys));
    running_keys{i} = (sorted_keys);
end

global_key_intersection = mintersect(running_keys{:});

for i = 1:length(lists)
    keys = (cellfun(get_key_callback,lists{i},'UniformOutput',0));
    [sorted_keys,sort_order]=sort((keys));
    [~,IA,~] = intersect(sorted_keys,global_key_intersection);
    new_lists{i} = lists{i}(sort_order(IA));
end

lists_lengths = cellfun(@length,new_lists);
assert(sum(lists_lengths==lists_lengths(1))==length(lists_lengths));


tmp=1;
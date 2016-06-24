function out = filter_empty_strings(string_list)

filter = @(tmp) ~isempty(tmp);
mask = cellfun(filter, string_list, 'UniformOutput',0);
out = string_list(cell2mat(mask));
function res = kv_regex_filter(regex,kv_map)

my_matcher = @(str)~isempty(regexp(str,regex));

matching_row_idxs = cellfun(my_matcher, kv_map(:,1));

res = kv_map(matching_row_idxs,:);

end
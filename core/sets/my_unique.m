function unique_values = my_unique(vec)

% in: a list 
%
% out: the unique values in the list, in the order with which they are encountered (as unique alone returns the unique values, but sorted)
%
% desc: as above.
%
% tags: #unique #sorting #deduplication #dedup

[~, idxs, ~] = unique(vec, 'first');
unique_values = vec(sort(idxs));
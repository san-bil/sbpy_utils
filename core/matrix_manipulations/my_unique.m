function unique_values = my_unique(vec)

% in: a vector
%
% out: a list of values with no repetitions, with values in the order with which they were encountered 
%      e.g. my_unique([5 5 5 3 3 3 4 61 61 61 99 99 92 92 1 1 6 6 6 6 6]) returns [5 3 4 61 99 92 1 6]
%
% desc: Use instead of unique() if you don't want your values sorted for you.
%
% tags: #duplicates #duplicateremoval #sequence #dups

[~, idxs, ~] = unique(vec, 'first');
unique_values = vec(sort(idxs));

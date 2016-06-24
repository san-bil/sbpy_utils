function out = row_mean_mat(in)

out = repmat(mean(in,2), [1 size(in,2)]);
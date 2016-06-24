function out = mat_2_rowcell(X)

out = mat2cell(X,ones(size(X,1),1),size(X,2));

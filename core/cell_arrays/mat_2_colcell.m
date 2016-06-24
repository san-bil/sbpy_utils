function out = mat_2_colcell(X)

out = mat2cell(X,size(X,1),ones(size(X,2),1));

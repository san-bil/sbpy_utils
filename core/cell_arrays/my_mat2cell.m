function [ y ] = my_mat2cell( x )

y = mat2cell(x,ones(size(x,1),1),ones(size(x,2),1));

end


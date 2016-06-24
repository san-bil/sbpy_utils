function is_column_vector = is_column_vector(vec)

% in: a vector/1d array
%
% out: bool specifying whether it is a column vector or not
%
% desc: (as above)
%
% tags: #defensive

is_column_vector = size(vec,1)>1 && size(vec,2)==1;

end

function is_row_vector = is_row_vector(vec)

% in: a vector/1d array
%
% out: bool specifying whether it is a row vector or not
%
% desc: (as above)
%
% tags: #defensive

is_row_vector = size(vec,2)>1 && size(vec,1)==1;

end

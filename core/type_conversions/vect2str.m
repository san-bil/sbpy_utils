function [ str ] = vect2str( vect )
%VECT2STR Summary of this function goes here
%   Detailed explanation goes here
str=['[ ' fold_string_carray(cellfun(@(x){[num2str(x) ', ']},my_mat2cell(vect))) ']'];

end


function [ output_args ] = index_array(x, varargin )

% in: numerical array, (multiple) array indices

% out: indexed array

% desc: Given the array indexes to be accessed, returns corresponding  
% elements in numerical array 'x'

% tags: #array-indexing 


output_args = x(varargin{:});


end


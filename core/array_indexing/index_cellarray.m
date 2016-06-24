function [ output_args ] = index_cellarray(x, varargin )

% in: cell array, (multiple) array indices 

% out: indexed array

% desc: Given the array indexes to be accessed, returns corresponding  
% elements in cell array 'x'

% tags: #array-indexing 
if(varargin{1}<1)

    output_args = x{end+varargin{:}};
else
    
    output_args = x{varargin{:}};

end


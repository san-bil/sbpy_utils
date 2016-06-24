function [ out ] = head( arr,idxs )

% in: numerical array; number of head elements

% out: first num_el elements of array 'arr'

% desc: Gives the first num_el elements of the array
% or the first element only if num_el isn't passed.

% tags: #array-indexing 

if(~exist('idxs','var')),idxs=1;end

out = arr(1:idxs);




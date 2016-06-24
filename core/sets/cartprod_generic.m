function [rarray,rows]= cartprod_generic(varargin)

%wants multiple cell arrays

list_sizes = cellfun(@(tmp)1:length(tmp), varargin,'UniformOutput',0);

scp = cartprod(list_sizes{:});

rarray = {};
rows = {};
for i = 1:size(scp,1)
   row = {};
   for j = 1:size(scp,2)
    row{j} = varargin{j}{scp(i,j)};
   end
   rows{end+1}=row;
   rarray = [rarray;row];
end



function out = cellcell(outer_dims, inner_dims,val)

if(~exist('val','var'))
    val=[];
end

out = cell(outer_dims);

total_size = prod(outer_dims);

for i = 1:total_size

    tmp = cell(inner_dims);
    tmp = cellfun_uo0(@(foo)val,tmp);
    out{i} = tmp;

end

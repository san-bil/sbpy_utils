function out = cellcell2(outer_dims, inner_dims)

out = cell(outer_dims);

total_size = prod(outer_dims);

for i = 1:total_size

    tmp = cell(inner_dims);
    out{i} = tmp;
end

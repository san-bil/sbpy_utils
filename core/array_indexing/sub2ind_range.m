function idxs = sub2ind_range(idx_range_1,idx_range_2,arrsize)

idxs = zeros(numel(idx_range_1)*numel(idx_range_2),1);
for i =1:length(idx_range_2)
    for j =1:length(idx_range_1)
        idxidx=(length(idx_range_2)*(i-1))+j;
        
        myres=((idx_range_2(i)-1)*arrsize(1))+idx_range_1(j);
        idxs(idxidx) = myres;
    end
end

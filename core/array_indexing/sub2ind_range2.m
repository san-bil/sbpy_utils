function idxs = sub2ind_range2(idx_range_1,idx_range_2,arrsize)

idxs = zeros(numel(idx_range_1)*numel(idx_range_2),1);
for i =1:length(idx_range_2)
    
    
        idxidx=(length(idx_range_2)*(i-1))+(1:length(idx_range_1));
        
        myres=((idx_range_2(i)-1)*arrsize(1))+idx_range_1(1:length(idx_range_1));
        idxs(idxidx) = myres;
    
end

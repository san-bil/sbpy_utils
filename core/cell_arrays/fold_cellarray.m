function acc=fold_cellarray(operator, cell_array)

acc = cell_array{1};

for i = 2:length(cell_array)
   
    elem = cell_array{i};
    acc = operator(acc,elem);
    
end

function out = fold_string_carray(string_carray)

out='';
for i = 1:length(string_carray)

    out = [out string_carray{i}];

end
    
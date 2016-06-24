function out = read_lines(file)

[~,res] = system(concat_cell_string_array({'cat',file},' ',1));

out = strsplit(res,'\n');
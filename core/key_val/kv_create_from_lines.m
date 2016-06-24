function map = kv_create_from_lines(lines,delimiter)

map = cell(length(lines),2);

for i = 1:length(lines)

    line = lines{i};
    split_line  = strsplit(line,delimiter);
    if(length(split_line)>2)
        warning(sprintf('More than one %s in line %d!', delimiter, i));
    end
    map{i,1} = split_line{1};
    map{i,2} = my_str_to_num(index_cellarray(my_regexp_matches(split_line{2},'\d*\.?\d*'),1));

end
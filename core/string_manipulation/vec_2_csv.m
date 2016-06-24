function csv=vec_2_csv(vec)

csv = concat_cell_string_array(cellfun_uo0(@(tmp)[num2str(tmp),','],my_mat2cell(vec)),' ');
csv = csv(1:end-1);
function easy_file_append_fast_num(arr,path)

text=my_cell2mat( force_fat_matrix( cellfun_uo0(@(tmp)sprintf('%d\n',tmp), my_mat2cell(force_fat_matrix(arr)) )));

easy_file_append_fast(text,path)
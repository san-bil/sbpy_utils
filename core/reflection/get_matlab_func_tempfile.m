function tmpfile_path=get_matlab_func_tempfile(ext)

mycaller=callerfunc();
tmp_folder = path_join('/tmp',['matlab_' mycaller]);
my_mkdir(tmp_folder);

tmpfile_path = create_increment_file(get_simple_date(), tmp_folder, ext, 1); 

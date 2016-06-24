function [out, tmpdir] = get_matlab_func_tempdir()

mycaller=callerfunc();
out = path_join('/tmp',['matlab_' mycaller]);
tmpdir = create_increment_folder(get_simple_date, out); 

function easy_file_append_fast(text,path)

touch(path);

fid = fopen(path, 'a');
fprintf(fid, text);
fclose(fid);
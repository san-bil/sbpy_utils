function fsize = get_file_size(file_path)

if(exist(file_path,'file'))
    tmp = dir(file_path);
    fsize = tmp.bytes;
else
    fsize=0;
end
function easy_file_append(text,path)

touch(path);

cmd = build_string_args({'echo',text,'>>',path});
system(cmd);
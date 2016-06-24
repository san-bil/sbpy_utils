function out = unix_finddir(folder, filter, find_opts)


cmd = build_cmd({'find',folder,'-type d',unix_pipe,'grep',filter});
[~,stdout] = system(cmd);
out = filter_empty_strings(strsplit(stdout,newline));
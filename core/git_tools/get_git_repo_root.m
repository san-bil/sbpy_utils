function [ out ] = get_git_repo_root(folder)

if(~exist('folder','var')),folder=pwd;end;

cmd =  build_cmd({ld_lib_path_fix,'cd',folder,cmdsep,'git rev-parse --show-toplevel'});

[~,out]=system(cmd);
out = strtrim(out);
end


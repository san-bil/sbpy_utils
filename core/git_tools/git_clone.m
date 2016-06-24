function git_clone(repo,parent_folder,host,ssh_key)

if(~exist('host','var')),host='localhost';end;
if(~exist('ssh_key','var')),ssh_key=default_ssh_key;end;

repo_folder = path_join(parent_folder,basename(repo));
cmd = concat_cell_string_array({'git','clone',repo,repo_folder},' ',1);

if(islocalhost(host))
    [res,out]=system(cmd);    
else
    [res,out]=ssh_call(cmd,host,ssh_key);
end

disp(out);
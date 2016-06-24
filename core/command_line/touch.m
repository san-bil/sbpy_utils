function touch(filepath,host,ssh_key)

if(~exist('host','var')),host='localhost';end;
if(~exist('ssh_key','var')),ssh_key=default_ssh_key;end;

my_mkdir(dirname(filepath),host,ssh_key);

cmd = concat_cell_string_array({'touch',filepath},' ',1);
if(islocalhost(host))
    system(cmd);
else
    [~,out]=ssh_call(cmd,host,ssh_key);
end
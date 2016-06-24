function chmod(filepath, permissions,host,ssh_key,varargin)

if(~exist('permissions','var')),permissions='755';end;
if(~exist('host','var')),host='localhost';end;
if(~exist('ssh_key','var')),ssh_key=default_ssh_key;end;

cmd = concat_cell_string_array({'chmod', permissions, filepath},' ',1);
if(islocalhost(host))    
    system(cmd);
else
    [res,out]=ssh_call(cmd,host,ssh_key);
end



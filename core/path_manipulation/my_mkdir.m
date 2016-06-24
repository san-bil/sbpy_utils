function dir_path = my_mkdir(dir_path,host,ssh_key)

% in: a directory path
%
% out: nada
%
% desc: creates the directory, if it doesn't exist already (mkdir already does this, but this
%       just prevents the cluttering warnings)
%
% tags: #file #path #extension #files

if(~exist('host','var')),host='localhost';end;
if(~exist('ssh_key','var')),ssh_key=default_ssh_key;end;


if(islocalhost(host))
    if(~exist(dir_path,'dir'))
        mkdir(dir_path)
    end    
else
    cmd = concat_cell_string_array({'mkdir','-p',dir_path},' ',1);
    [res,out]=ssh_call(cmd,host,ssh_key);
    disp(out);
end
    
    

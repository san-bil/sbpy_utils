function rsync(src, dst, rsync_args,host,ssh_key, direction)

if(~exist('host','var')),host='localhost';end;
if(~exist('ssh_key','var')),ssh_key=default_ssh_key;end;
if(~exist('direction','var')),direction='push';end;
if(~exist('rsync_args','var')),rsync_args={};end;



rsync_args_string = concat_cell_string_array(rsync_args,' ',1);


if(islocalhost(host))
    cmd = concat_cell_string_array({'rsync','-auzh',rsync_args_string,src,dst},' ',1);

else
    remote_rsync_args = ['-e "ssh -o IdentityFile=' ssh_key '"'];
    
    if(strcmp(direction,'push'))
        dst = [host ':' dst];
    elseif(strcmp(direction,'pull'))
        src = [host ':' src];
    else
        error('rsync ''direction'' argument must be ''push'' or ''pull''')
    end
    
    cmd = concat_cell_string_array({ld_lib_path_fix,'rsync','-auzh',rsync_args_string,remote_rsync_args,src,dst},' ',1);

end
disp(cmd);
[~,msg]=system(cmd);
tmp=1;
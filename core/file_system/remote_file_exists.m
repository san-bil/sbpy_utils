function out = remote_file_exists(remote_file,remote_host,ssh_key)


if(islocalhost(remote_host))

    out = exist(remote_file,'file');
    
else
    
    if(~exist('ssh_key','var')),ssh_key=default_ssh_key;end;

    cmd = ['if [[ -f ' remote_file ' ]];then echo 1;else echo 0;fi'];

    [~,stdout] = ssh_call(cmd,remote_host,ssh_key);

    out = my_str_to_num(index_cellarray(parse_stdout(stdout),1));
end
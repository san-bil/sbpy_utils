function res = is_ssh_host_responding2(host_url)

string_args = {'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 ',host_url,'"echo u_up  ;echo ENDSSH"'};
cmd =  [ld_lib_path_fix build_string_args(string_args)];
[~,stdout] =system(cmd);
stdout_lines = filter_empty_strings( strsplit(stdout,'\n') );

res = ~any(cell2mat(cellfun_uo0(@(tmp)logical(length(regexp(tmp,'Connection timed out'))),stdout_lines)));


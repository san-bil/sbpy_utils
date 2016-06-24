function [res,out] = ssh_call(cmd,host,ssh_key)

cmd_bits = {ld_lib_path_fix,'ssh -i ',ssh_key,host,['"' cmd '"']};

cmd = concat_cell_string_array(cmd_bits,' ',1);

[res,out] = system(cmd);
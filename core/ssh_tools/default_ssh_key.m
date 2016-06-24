function default_ssh_key_path = default_ssh_key()

default_ssh_key_path = path_join(home_folder,'.ssh','id_rsa');

if(~exist(default_ssh_key_path,'file'))
    warning_msg = [mfilename ': Using ' default_ssh_key_path ' as the default ssh key, however it does not exist!\n'];
    warning_msg = [warning_msg '\t\t\tYou''ll need to create one using ssh-keygen, and then push it to all compute nodes using ssh-copy-id.'];
    warning_msg = [warning_msg '\t\t\tSee e.g. http://www.thegeekstuff.com/2008/11/3-steps-to-perform-ssh-login-without-password-using-ssh-keygen-ssh-copy-id for details.'];
    warning(sprintf(warning_msg));
end
function default_config = default_ssh_config()

default_config = path_join(home_folder,'.ssh','config');

touch(default_config);
 


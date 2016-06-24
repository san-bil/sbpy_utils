import os
import platform
import command_line
from command_line import get_default_ssh_key,mkdir_p2,my_system
from file_system import create_increment_file,get_python_func_tempdir
from my_io import my_save
from my_datetime import get_simple_date


def rsync(src, dst, rsync_args=[], host='localhost', ssh_key=os.path.join(os.path.expanduser('~'),'.ssh/id_rsa'), direction='push'):
    
        
    rsync_args_string = ' '.join(rsync_args)
    
    
    if(host in [platform.node(),'localhost']):
        cmd = ' '.join(['rsync','-auzh',rsync_args_string,src,dst])
    
    else:
        remote_rsync_args = '-e "ssh -o IdentityFile='+ssh_key+'"'
        
        if(direction=='push'):
            dst = host+':'+dst
        elif((direction=='pull')):
            src = host+':'+src
        else:
            raise ValueError('rsync "direction" argument must be "push" or "pull"')
        
        
        cmd = ' '.join(['rsync','-auzh',rsync_args_string,remote_rsync_args,src,dst]);
    
    out = my_system(cmd);
    return out


def rsyncs(inputs, dst, rsync_args, *args):

    for src in inputs:
        rsync(src, dst, rsync_args, *args)
        
def save_and_rsync(save_and_rsync_host,save_and_rsync_data_path,save_and_rsync_var_map,save_and_rsync_ssh_key=get_default_ssh_key()):
    
    save_and_rsync_tmp_folder=get_python_func_tempdir()[0];
    mkdir_p2(save_and_rsync_tmp_folder);
    save_and_rsync_tmpfile_path,_ = create_increment_file(get_simple_date(), save_and_rsync_tmp_folder, 'p'); 
    my_save(save_and_rsync_var_map,save_and_rsync_tmpfile_path);
    save_and_rsync_direction='push';
    rsync(save_and_rsync_tmpfile_path, save_and_rsync_data_path, [],save_and_rsync_host,save_and_rsync_ssh_key, save_and_rsync_direction)
    os.remove(save_and_rsync_tmpfile_path)



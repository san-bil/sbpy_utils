import sys
import subprocess
from subprocess import check_output
import os
import platform
from  file_system import mkdir_p
from string_manipulation import filter_empty_strings

def get_default_ssh_key():
    return os.path.join(os.path.expanduser('~'),'.ssh/id_rsa')

def my_system(cmd):

    out = check_output(cmd, stderr=subprocess.STDOUT, shell=True )
    return out

def chmod(filepath, permissions='755',host='localhost',ssh_key=get_default_ssh_key()):

    
    cmd = ' '.join(['chmod', permissions, filepath]);
    if(islocalhost(host)):    
        res=my_system(cmd);
    else:
        res=ssh_call(cmd,host,ssh_key);
        
    return res


def ssh_call(cmd,host,ssh_key=get_default_ssh_key(),opts=''):
    
    cmd_bits = ['ssh -i ',ssh_key,host,'"'+cmd+'"']

    cmd = ' '.join(cmd_bits)
    
    return my_system(cmd);


def touch(filepath,host='localhost',ssh_key=get_default_ssh_key()):
        
    mkdir_p2(os.path.dirname(filepath),host,ssh_key);
    
    cmd = ' '.join(['touch',filepath])
    if(islocalhost(host)):
        my_system(cmd);
    else:
        out=ssh_call(cmd,host,ssh_key);
    



def mkdir_p2(dir_path,host='localhost',ssh_key=get_default_ssh_key()):

    if(islocalhost(host)):
        mkdir_p(dir_path)
    else:
        cmd = ' '.join(['mkdir','-p',dir_path])
        out=ssh_call(cmd,host,ssh_key)
        print(out)
    
def easy_file_append(text,path):
    touch(path)
    cmd = ' '.join(['echo',text,'>>',path])
    my_system(cmd);    

def is_ssh_host_responding2(host_url):
    
    string_args = ['ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 ',host_url,'"echo u_up  ;echo ENDSSH"'];
    cmd =  ' '.join(string_args);
    cmd_res = my_system(cmd);
    stdout_lines = filter_empty_strings( cmd_res.split('\n') )
    res = len([f for f in stdout_lines if ('Connection timed out' in f or 'Could not resolve' in f) ])==0
    return res


def islocalhost(host):
    return (host=='localhost') or not (isremotehost(host))
    
def isremotehost(host):
    return (not (host==get_local_hostname()))

def get_local_hostname():
    return platform.node()

def get_local_os():
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        plat='linux'
    elif _platform == "darwin":
        plat='mac'
    elif _platform == "win32":
        plat='windows'    
    return plat


def remote_file_exists(remote_file,remote_host,ssh_key=get_default_ssh_key()):

    if(islocalhost(remote_host)):
        out = os.path.isfile(remote_file)
    else:
        cmd = 'if [[ -f '+remote_file+' ]];then echo 1;else echo 0;fi'
        cmd_res = filter_empty_strings(ssh_call(cmd,remote_host,ssh_key).split('\n'))
        out = float(cmd_res[0])
    return out


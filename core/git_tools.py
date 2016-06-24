import os,sys
from command_line import my_system,ssh_call,islocalhost,get_default_ssh_key


def git_clone(repo,parent_folder,host='localhost',ssh_key=get_default_ssh_key()):

    repo_folder = os.path.join(parent_folder,os.path.basename(repo));
    cmd = ' '.join(['git','clone',repo,repo_folder])
    
    if(islocalhost(host)):
        cmd_res=system(cmd);    
    else:
        cmd_res=ssh_call(cmd,host,ssh_key);

    print(cmd_res);
    
    
def get_git_repo_root(folder=os.getcwd()):
    cmd = ' '.join(['cd',folder,'&&','git rev-parse --show-toplevel']);
    cmd_res=my_system(cmd).strip()
    return cmd_res

def cwd_is_valid_git_repo():
    x=get_git_repo_root(os.getcwd());
    isvalid='fatal: Not a git repository' in x
    return isvalid
function isvalid = cwd_is_valid_git_repo()

x=get_git_repo_root;

isvalid=isempty(regexp(x,'fatal: Not a git repository', 'once'));
function lines= search_codebase(search_term, search_root, linewise)

if(nargin==0)
    fprintf('\n\tUsage: search_codebase(search_term, search_root, linewise)\n\n')
    return
end

if(nargin==1)
    search_root = pwd;
end

if(~exist('linewise','var'));linewise=0;end;



if(~linewise)
    search_term = ['''*' search_term '*'''];
    cmd = build_string_args({'find',search_root,'-iwholename',search_term});

else
    cmd = build_string_args({'grep','-R',search_term,search_root});
    
end

[~,stdout]=system_e(cmd);

lines = parse_stdout(stdout)';
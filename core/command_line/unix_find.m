function out = unix_find(folder, filter,find_opts,follow_links,actions)

if(~exist('find_opts','var'));
    find_opts = {'-type','f','-name',['"*' filter '*"']};
else
    if(~ismember('-name',find_opts))
        find_opts = [find_opts {'-name',['"*' filter '*"']}];
    end
end;

if(~exist('actions','var'))
    actions={};
end

if(~exist('follow_links','var'))
    follow_links_str='-L';
elseif(follow_links)
    follow_links_str='-L';
elseif(~follow_links)
    follow_links_str='';
end

opts_str = build_cmd(find_opts);

cmd = build_cmd({'find',follow_links_str,folder,opts_str,actions{:}});
[~,stdout] = system(cmd);
out = filter_empty_strings(strsplit(stdout,newline))';

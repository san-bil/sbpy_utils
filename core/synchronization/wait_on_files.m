function wait_on_files(files_list,holding_time)

% in: a list of file paths
%     a waiting period between file-existence checks
%
% out: nada.
%
% desc: Every holding_time seconds, the function checks for the presence of all the files in files_list.
%       As soon as they all exist, the function exits. Used for sending off a bunch of jobs via the shell,
%       and sychronizing by waiting for the results, instead of waiting for each job synchronously.
%
% tags: #synchronization #jobs #condor #shell
if(~exist('holding_time', 'var'))
   holding_time = 5; 
end


fprintf('%s waiting on: \n',callerfunc());
disp_cellstr( cellfun_uo0(@(tmp)['       ' tmp],files_list));

flag = 1;

while(1)
    
    for i=1:length(files_list)
        flag = flag && exist(files_list{i},'file');
    end
    
    if(flag)
        return;
    else
        flag=1;
    end
    
    pause(holding_time);
    
    tic;
    while(1)
        inv_time = toc;
        if(inv_time>1)
            break;
        end
    end
    
end

fprintf('%s has finished waiting!\n',callerfunc());

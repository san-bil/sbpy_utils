function conditional_pause(stop_file)

if(~exist('stop_file','var'))
    [~,home_folder]=system('echo $HOME');
    stop_file = [strtrim(home_folder) filesep 'matlab_stop'];
end

if(exist(stop_file,'file'))
    dbstop in conditional_pause_inner.m
else
    dbclear in conditional_pause_inner.m
end


conditional_pause_inner();
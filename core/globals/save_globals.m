function saveGlobalVariables( mat_file_path )

% in: a full file path, ending in .mat
%
% out: nada
%
% desc: saves all the current global variables to the specified mat file
%
% tags: #file #globalvariables #stateful #savestate

list_global_vars = who('global');



for i = 1:length(list_global_vars)

    varName = list_global_vars{i};
    
    eval(['global ', varName])
    
    save(mat_file_path,varName,'-append')

end

end


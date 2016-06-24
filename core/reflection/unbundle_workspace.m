
reflection_curr_vars = kv_getkeys(workspace_dict);
for ijkl = 1:length(reflection_curr_vars)
    if(~(strcmp('reflection_curr_vars',reflection_curr_vars{ijkl})))
        eval([reflection_curr_vars{ijkl} '=' 'kv_get(''' reflection_curr_vars{ijkl}  ''',workspace_dict);'])
    end
end

clear workspace_dict
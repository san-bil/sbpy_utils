
reflection_curr_vars = whos;
workspace_dict = {};
for ijkl = 1:length(reflection_curr_vars)
    workspace_dict = kv_set(reflection_curr_vars(ijkl).name,eval(reflection_curr_vars(ijkl).name),workspace_dict);
end
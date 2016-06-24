function options = add_to_stackignore(options)
stack = dbstack;
options = kv_append_val('stackignore',stack(2).name,options);
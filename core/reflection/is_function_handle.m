function out = is_function_handle(in)

out = strcmp(class(in),'function_handle');

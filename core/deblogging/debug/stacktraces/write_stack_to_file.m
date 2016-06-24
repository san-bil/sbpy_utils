function write_stack_to_file(file_path,options)

stack = dbstack();
options = add_to_stackignore(options);
stackignore = kv_get('stackignore',options);

stack_file_ID = fopen(file_path,'w');
for i = 1:length(stack)
    stackframe_name = stack(i).name;
    if(~ismember(stackframe_name, stackignore))
        fprintf(stack_file_ID,'%s\n',stackframe_name);
    end
end




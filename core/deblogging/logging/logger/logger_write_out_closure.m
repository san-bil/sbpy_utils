function logger_write_out_closure(logger, name, closure)

root_node = logger.root_node;
my_stack = dbstack;
my_stack = flipud(my_stack(2:end));
curr_dir = cat_struct_fieldname(my_stack, 'name', '/');
fq_curr_dir = [root_node filesep curr_dir];
my_mkdir(fq_curr_dir);

out = evalc(['closure()']);

[fname, fnumber, fhandle] = create_increment_file(input_var_name, fq_curr_dir, 'log', 0);

caller_line = my_stack(2).line;
if(fnumber>1)
	fprintf(fhandle, '%s: \n', caller_line);
	fprintf(fhandle, '-----------------------------------------------------\n');
end

fprintf(fhandle, '%s\n', input_var_name);
fprintf(fhandle, '-----------------------------------------------------\n');


fprintf(fhandle, '%s\n', out);

fclose(fhandle);

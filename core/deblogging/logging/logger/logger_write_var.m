function logger_write_var(logger, input_var)

root_node = logger.root_node;
curr_dir = logger.stack{end};
fq_curr_dirr = [root_node filesep curr_dir];

input_var_name = inputname(input_var);
out = evalc([' '' '+input_var_name+' ''  ']);

[fname, fnumber, fhandle] = create_increment_file(input_var_name, fq_curr_dir, 'log', 0);

my_stack = dbstack;
caller_line = my_stack(2).line;
if(fnumber>1)
	fprintf(fhandle, '%s: \n', caller_line);
	fprintf(fhandle, '-----------------------------------------------------\n');
end

fprintf(fhandle, '%s', out);

close(fhandle);

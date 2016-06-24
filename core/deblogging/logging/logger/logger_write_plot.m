function logger_write_plot(logger, name, plot_handle, other_handles, options)

root_node = logger.root_node;
curr_dir = logger.stack{end};
fq_curr_dirr = [root_node filesep curr_dir];

my_stack = dbstack;
caller_line = my_stack(2).line;
[fname, fnumber] = create_increment_file([name '_line_' num2str(caller_line) ], fq_curr_dir, 'log', 1);

fig_handle = figure('Visible', 'off');
plot_handle();

for i = 1:length(other_handles)
	tmp_handle = other_handles{i};
	tmp_handle(gca);
end

height = kv_get('height',options,8);
width = kv_get('width',options,13);

hgexport(fig_handle, fname, hgexport('factorystyle'), 'Format', 'png', 'Resolution', 300, 'Width', width, 'Height', height, 'Units', 'inch');

close(fig_handle);

function save_and_rsync(save_and_rsync_host,save_and_rsync_data_path,save_and_rsync_var_map,save_and_rsync_ssh_key)

if(~exist('ssh_key','var')),save_and_rsync_ssh_key=default_ssh_key;end;

save_and_rsync_tmp_folder=get_matlab_func_tempdir();
my_mkdir(save_and_rsync_tmp_folder);
save_and_rsync_tmpfile_path = create_increment_file(get_simple_date(), save_and_rsync_tmp_folder, 'mat', 1); 

kv_unpack(save_and_rsync_var_map);
save_and_rsync_var_map_keys = save_and_rsync_var_map(:,1)';

save(save_and_rsync_tmpfile_path,save_and_rsync_var_map_keys{:},'-v7.3');

save_and_rsync_direction='push';
rsync(save_and_rsync_tmpfile_path, save_and_rsync_data_path, {},save_and_rsync_host,save_and_rsync_ssh_key, save_and_rsync_direction)
delete(save_and_rsync_tmpfile_path)
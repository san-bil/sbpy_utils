function file_path = get_multipie_file_path(opts)


session = ternary_cond(~strcmp(kv_get('session', opts),'*'),@(tmp)zfill(tmp,2),@(tmp)tmp,{kv_get('session', opts)});
aug_session = ['session' session];
subject = ternary_cond(~strcmp(kv_get('subject', opts),'*'),@(tmp)zfill(tmp,3),@(tmp)tmp,{kv_get('subject', opts)});
expression = ternary_cond(~strcmp(kv_get('expression', opts),'*'),@(tmp)zfill(tmp,2),@(tmp)tmp,{kv_get('expression', opts)});

camera_name = kv_get('camera', opts);
real_camera_id = kv_get(camera_name,multipie_camera_locations());

%lighting = ternary_cond(~strcmp(kv_get('lighting', opts),'*'),@(tmp)zfill(tmp,2),@(tmp)tmp,{kv_get('lighting', opts)});
default_lighting=num2str(kv_get(real_camera_id,multipie_aligned_camera_flash_pairs()));
tmp_l=kv_get('lighting', opts,default_lighting);
lighting = ternary_cond(~strcmp(tmp_l,'*'),@(tmp)zfill(tmp,2),@(tmp)tmp,{tmp_l});    

filename_builder = {subject,session, expression,strrep(real_camera_id,'_',''),lighting};
file_name = [concat_cell_string_array(filename_builder,'_',1),'.png'];

regex_builder = {'/vol/hci2/Databases/video/MultiPIE',aug_session,'png',subject,expression,real_camera_id, file_name};
file_path = concat_cell_string_array(regex_builder,filesep,1);


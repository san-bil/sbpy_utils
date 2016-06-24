function img = wget_image(img_url)

tmp_dir = ['/tmp/sbmat_image/wget' filesep get_simple_date()];
my_mkdir(tmp_dir);
output_file = [tmp_dir filesep basename(img_url)];

cmd_pieces = {'unset LD_LIBRARY_PATH && unset OSG_LD_LIBRARY_PATH && wget','--quiet',img_url,'–output-document','output_filename',output_file};
cmd = concat_cell_string_array(cmd_pieces,' ',1);

[~,res] = system(cmd);

img = imread(output_file);
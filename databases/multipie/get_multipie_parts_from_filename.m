function out = get_multipie_parts_from_filename(filepath)

tmp = basename(filepath);

parts = strsplit(tmp,'_');

subject = str2num(parts{1});
session = str2num(parts{2});
expression = str2num(parts{3});
camera = [parts{4}(1:2) '_' parts{4}(3)];

lighting = str2num(strrep(parts{5},'.png',''));

out = kv_create(session,subject,expression,camera,lighting);

%   /vol/hci2/projects/Sanjay-dnd/databases/multipie_crop_test_out/right/273_03_01_041_09.png
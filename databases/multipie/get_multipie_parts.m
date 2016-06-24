function parts = get_multipie_parts(filepath)

tmp = strsplit(filepath,filesep);

session = str2num(strrep(tmp{7},'session',''));


subject = str2num(tmp{9});
expression = str2num(tmp{10});
camera = (tmp{11});

filename = tmp{end};
tmp2 = strsplit(filename,'_');
lighting = str2num(strrep(tmp2{end},'.png',''));

parts = kv_create(session,subject,expression,camera,lighting);
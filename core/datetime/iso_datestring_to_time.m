function out = iso_datestring_to_time(in)

script_parts = {
'import dateutil.parser',...
['x = dateutil.parser.parse' addbrack(add_single_quotes(in))],...
'print x.hour',...
'print x.minute',...
'print x.second',...
'print x.microsecond'
};

script = add_double_quotes(concat_cell_string_array(script_parts,';',1));

cmd = build_cmd({'python -c',script});

[~,stdout] = system(cmd);

tmp = filter_empty_strings(strsplit(stdout,newline));

hour = str2num(tmp{1});
minute = str2num(tmp{2});
second = str2num(tmp{3});
millis = str2num(tmp{4})/1000;

out = kv_create(hour,minute,second,millis);
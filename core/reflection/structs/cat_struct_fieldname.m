function out = cat_struct_fieldname(struct_array, fieldname, delim)

out = [];

for i = 1:length(struct_array)

	out = [out delim struct_array(i).(fieldname)];

end
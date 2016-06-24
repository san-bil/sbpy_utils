function out = str(x)

if(isnumeric(x))
    out = num2str(x);
elseif(ischar(x))
    out = x;
elseif(iscell(x))
    out = concat_cell_string_array(x,'delim',1);
else
    error('wrong type');
end
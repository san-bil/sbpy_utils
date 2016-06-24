function out = my_str_to_num(x)

if(isnumeric(x))
    out = x;
elseif(ischar(x))
    out = str2num(x);
else
    error('wrong type');
end
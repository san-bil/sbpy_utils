function out = tostr(in)

if(ischar(in))
    out=in;
elseif(isnumeric(in))
    out = num2str(in);
elseif(iscell(in))
    out = concat_cell_string_array(in,',',1);
elseif(is_function_handle(in))
    out = func2str(in);
else
    error([mfilename ': Not sure how to stringify input.'])
end

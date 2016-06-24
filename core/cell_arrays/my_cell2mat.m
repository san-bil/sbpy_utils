function out = my_cell2mat(in)

if(iscell(in))
    out = cell2mat(in);
else
    out = in;
end
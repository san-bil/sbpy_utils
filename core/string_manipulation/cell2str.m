function out=cell2str(in)

if(iscell(in))
    out = in{1};
else
    out=in;
end
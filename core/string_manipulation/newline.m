function out =newline()

if(ispc)
    out = '\r\n';
elseif(isunix)
    out = '\n';
end
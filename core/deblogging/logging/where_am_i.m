function CallerFileNameWithPath = where_am_i(do_disp)

mystack = dbstack;
CallerFileNameWithPath = which(mystack(2).file);

if(exist('do_disp','var') && do_disp==1)
    disp(CallerFileNameWithPath)
end

end
function [ out ] = retval_idxr( f_handle,idx )

% This is totally not my fault.

if(idx==1)
    out=f_handle();
elseif(idx==2)
    [~,out]=f_handle();
elseif(idx==3)
    [~,~,out]=f_handle();
elseif(idx==4)
    [~,~,~,out]=f_handle();
elseif(idx==5)
    [~,~,~,~,out]=f_handle();
elseif(idx==6)
    [~,~,~,~,~,out]=f_handle();
elseif(idx==7)
    [~,~,~,~,~,~,out]=f_handle();
end


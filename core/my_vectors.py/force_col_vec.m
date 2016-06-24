function out=force_col_vec(in)

if(size(in,2)>size(in,1) && size(in,1)==1)
    
    out = in';

elseif(size(in,1)>size(in,2) && size(in,2)==1)

    out=in;
else
    out=in;

end

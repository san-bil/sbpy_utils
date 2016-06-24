function out=force_skinny_matrix(in)

if(size(in,2)>size(in,1))
    
    out = in';

elseif(size(in,1)>size(in,2))

    out=in;
else
    out=in;

end

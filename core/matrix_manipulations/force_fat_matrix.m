function out=force_fat_matrix(in)

if(size(in,1)>size(in,2))
    
    out = in';

elseif(size(in,2)>size(in,1))

    out=in;
else
    out =in;

end

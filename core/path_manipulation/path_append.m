function c = path_append(a,b)

if(isempty(a) && isempty(b))
    
    c ='';

else
    
    c = [a filesep b];

end
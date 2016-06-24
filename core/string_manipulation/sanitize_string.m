function [ y ] = sanitize_string( x, sanitizer )

if(~exist('sanitizer','var'))
    sanitizer='_';
end
y=lower(x);

y=strrep(y,'    ',sanitizer);
y=strrep(y,'   ',sanitizer);
y=strrep(y,'  ',sanitizer);
y=strrep(y,' ',sanitizer);

end


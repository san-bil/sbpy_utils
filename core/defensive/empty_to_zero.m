function [ y ] = empty_to_zero( x )

% in: numeric array
%
% out: non-empty numeric array
%
% desc: if x is empty, changes value to 0
%
% tags: #emptyarray #defensive

if(isempty(x))
    y=0;
else
    y=x;
end

end


function i_s = zfill( i_s, n )

% in: a numeric/string value
%
% out: string of passed number, padded to desired string length with zeros
%
% desc: as above
%
% tags: #string #strings #numeric
if(isnumeric(i_s))
    i_s = num2str( i_s );
end

while length( i_s ) < n
    i_s = [ '0' i_s ];
end

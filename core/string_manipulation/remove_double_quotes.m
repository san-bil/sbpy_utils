function [ output_string ] = remove_double_quotes( input_string )

% in: a string
%
% out: a string, removed of all double quotes
%
% desc: as above
%
% tags: #string #strings #cleaning

output_string = regexprep(input_string,'"','');


end


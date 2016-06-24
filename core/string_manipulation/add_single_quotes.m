function [ output_string ] = add_single_quotes( input_string )

% in: a string
%
% out: the string wrapped in double quotes
%
% desc: as above. Useful for calls to the shell, e.g. if paths have unescaped spaces in them
%
% tags: #string #strings #quotes #escaping

output_string = ['''',input_string,''''];


end


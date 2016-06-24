function [ new_path ] = fix_path_slashes( path,no_trailing )

% in: file path
%
% out: file path with forwards slashes, for Unix
%
% desc: changes file path slashes to Unix-style (backwards)
%
% tags: #path #slashes #location #file #files

new_path = regexprep(path,'\','/');

if(exist('no_trailing','var') && no_trailing==1)

else
    if(~strcmp(new_path(end),'/'))
        new_path = [new_path,'/'];
    end
end



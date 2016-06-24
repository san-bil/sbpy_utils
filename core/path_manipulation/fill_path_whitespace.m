function out = fill_path_whitespace(input)

% in: a file name
%
% out: the file's extension
%
% desc: as above.
%
% tags: #file #path #extension #files

out = strrep(input,' ','_');

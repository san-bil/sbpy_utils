function [ stripped ] = strip_extension( filename )

% in: a file name
%
% out: the file's extension
%
% desc: as above.
%
% tags: #file #path #extension #files

[stripped,extension]=split_filename( filename );

end


function [ parent_folder_path,file_name] = get_parent_dir( file_path )

% in: a file path
%
% out: the containing folder, and the filename
%
% desc: as above.
%
% tags: #file #path #extension #files #parentdir #directory

file_path = strrep(file_path,'\','/');

idx = max(strfind(file_path,'/'));

parent_folder_path = file_path(1:idx-1);
if(idx>0)
    file_name = file_path(idx+1:end);
else
    file_name=file_path;
end


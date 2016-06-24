function [ new_folder_path,new_folder_idx ] = create_increment_folder( folder_prefix, parent_folder )

% in: file prefix string;
%     folder in which to create file
%     file format extension
%
% out: the new folder's path
%
% desc: Given a folder and a regex, returns the next member in the the folder sequence
%   e.g. given a folder '~/foo' (which contains /sequence_1/) and 'sequence_', creates '~/foo/sequence_2/'
%   and returns its path
%
% tags: #file #files #folders #directories #bookkeeping #wrappers

    parent_folder = fix_path_slashes(parent_folder);
    folders = dir(parent_folder);
    matching_folders_numbers = [];
    
    for i = 1:length(folders)
        folder_name = folders(i).name;
        contains_pattern = regexpi(folder_name, [folder_prefix,'.*']);

        if(~isempty(contains_pattern))
            split_result = str2num(regexprep(folder_name,folder_prefix,''));
            matching_folders_numbers = [matching_folders_numbers split_result];
        end
    end
        
    matching_folders_numbers = sort(matching_folders_numbers);
    
    if(~isempty(matching_folders_numbers))
        highest_folder = matching_folders_numbers(end);
    else
        highest_folder = 0;
    end
	new_folder_idx=highest_folder+1;
    new_folder_path = [parent_folder,folder_prefix,int2str(new_folder_idx)];
    
    my_mkdir(new_folder_path);
end


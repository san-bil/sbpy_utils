function [ new_file_path,file_number,new_file_handle ] = create_increment_file( file_prefix, parent_folder, target_file_ext, dont_fopen )

% in: file prefix string;
%     folder in which to create file
%     file format extension
%
% out: the new file's path, 'sequence' number, and file handle
%
% desc: Given a folder and a file_prefix (glob style), returns the next member in the the file sequence
%   e.g. given a folder '~/foo' (which contains output_1.txt) and 'output_', returns '~/foo/output_2.txt',
%   its 'sequence' number, and its file handle
%
% tags: #file #files #bookkeeping #wrappers



    parent_folder = fix_path_slashes(parent_folder);
    files = dir(parent_folder);
    matching_files_numbers = [];
    
    for i = 1:length(files)
        file_name = files(i).name;
        contains_pattern = regexpi(file_name, [file_prefix,'.*']);

        if(~isempty(contains_pattern))
            post_pattern=regexprep(file_name,file_prefix,'');
            period_idx = regexpi(post_pattern,'\.');
            file_format= post_pattern(period_idx+1:end);
            if(strcmp(target_file_ext,file_format))
                file_number = str2num(post_pattern(1:(period_idx-1)));
                matching_files_numbers = [matching_files_numbers file_number];
            end
        end
    end
        
    matching_files_numbers = sort(matching_files_numbers);
    
    if(~isempty(matching_files_numbers))
        highest_file = matching_files_numbers(end);
    else
        highest_file = 0;
    end
	file_number = highest_file+1;
    new_file_path = [parent_folder,file_prefix,int2str(file_number) '.' target_file_ext];
    
    if(exist('dont_fopen','var') && dont_fopen==1)
        
    elseif(exist('dont_fopen','var') && dont_fopen==2)
        new_file_handle = fopen(new_file_path,'a');
        fclose(new_file_handle);
    else
        new_file_handle = fopen(new_file_path,'a');
    end
    
end


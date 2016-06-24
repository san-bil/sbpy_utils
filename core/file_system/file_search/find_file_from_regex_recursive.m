function [ matching_files, fq_file_names ] = find_file_from_regex_recursive( folder,regex, verbose)

% in: a full folder path;
%      a regex string to match filenames against
%
% out: a list of files contained in that folder, matching the given regex
%
% desc: as above.
%
% tags: #filelist #filesearch #regex #files #file #filenames #search #folder

matching_files = {};
fq_file_names = {};

files = dirrec(strtrim(folder));



for i = 1:length(files)

    if(nargin>2 && verbose==1)
        fprintf('%s\n',files{i});
    end
    
    
    if(~isempty(regexp(files{i},regex)))
        matching_files{end+1} = files{i};
        fq_file_names{end+1} = [folder filesep files{i}];
    end
end


end


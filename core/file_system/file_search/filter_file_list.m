function [ filtered_matching_files ] = filter_file_list( files, regexes, reject_regexes, verbose )

% in: a full folder path;
%      a list of regexes string to match filenames against
%      a list of regexes string to reject filenames against
%
% out: a list of files contained in that folder, matching the first regex set, and not matching the second regex set 
%
% desc: as above.
%
% tags: #filelist #filesearch #regex #files #file


filtered_matching_files={};


for i = 1:length(files)

    if(nargin>3 && verbose==1)
        fprintf('%s\n',files(i).name);
    end
    
    file_name = files{i};
    flag = 0;
    
    for j = 1:length(regexes)
        contains_regex = ~isempty(regexp(file_name,regexes{j}));
        flag = flag || contains_regex;
    end
    
    for k = 1:length(reject_regexes)
        does_not_contain_regex = isempty(regexp(file_name,reject_regexes{k}));
        flag = flag && does_not_contain_regex;
    end
    
    if(flag)
    	filtered_matching_files{end+1} = file_name;
    end
    
end


end


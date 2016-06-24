function sorted_subfolders = fetch_files_by_date(folder)

% in: a full folder path
%
% out: a list of files contained in that folder, sorted by modification date
%
% desc: as above.
%
% tags: #filelist #filesearch #file #files

% if(~strcmp(folder([1 2]),'\\'))
%     filesep = '/';
%     folder  = strrep(folder,'\','/');
% end

subfolders_structs = dir(folder);
num_experiments = size(subfolders_structs,1);

subfolders={};

date_nums = [];

% 3 to skip . and ..
for i = 3:num_experiments
    
    subfolders = [subfolders;{subfolders_structs(i).name}];
    
    date_nums = [date_nums;subfolders_structs(i).datenum];
    
end


[sorted_datenums,sorted_datenums_idxs] = sort(date_nums);


sorted_subfolders = subfolders(sorted_datenums_idxs);

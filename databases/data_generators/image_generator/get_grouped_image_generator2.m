function grouped_image_generator = get_grouped_image_generator2(folder, glob_matchers,grouper,use_cache_file,ban_files, ban_list, opts)

if(~exist('opts','var'))
    opts = {};
end

igs = {};
for i = 1:length(glob_matchers)
    
    ig = get_image_generator(folder, glob_matchers{i},use_cache_file, ban_files{i}, ban_list, opts);
    igs{end+1}=ig;
    
end

gig = GroupedImageGenerator2(igs{:});
print_log_message(2,2,'Grouping lists for GroupedImageGenerator2\n');

if(length(glob_matchers)>1)
    grouped_image_generator = gig.group_lists(grouper);
else
    grouped_image_generator=gig;
end
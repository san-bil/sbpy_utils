function grouped_image_generator = get_grouped_image_generator(folder, glob_matchers,grouper,use_cache_file,ban_files, ban_list)

igs = {};
for i = 1:length(glob_matchers)
    
    ig = get_image_generator(folder, glob_matchers{i},use_cache_file, ban_files{i}, ban_list);
    igs{end+1}=ig;
    
end

gig = GroupedImageGenerator(igs{:});

grouped_image_generator = gig.group_lists(grouper);
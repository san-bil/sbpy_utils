function image_generator = get_image_generator(folder, glob_matcher,use_cache_file, ban_file, ban_list, opts)

conservative=1;
if(~use_cache_file)
    
    cmd = concat_cell_string_array({'find',kv_get('follow_symlinks',opts,''),folder,'-wholename',['"' glob_matcher '"']},' ',conservative);
    [~,res] = system(cmd);
    lines = strsplit(res,'\n');

else
    
    cache_file = kvg('file_list_cache',opts,path_join(folder,'file_list.txt'));
    regex_matcher=strrep(glob_matcher,'/','\/');
    regex_matcher=strrep(regex_matcher,'.','\.');
    regex_matcher=['''' strrep(regex_matcher,'*','.*') ''''];
    
    cmd = concat_cell_string_array({'cat',cache_file,unix_pipe,'grep -P',regex_matcher,'| sed -e "s/^.*$/&1\n/"'},' ',conservative);
    [~,res] = system(cmd);
    lines = strsplit(res,'1\n');
    
end
lines = filter_empty_strings(lines);
clean_lines = cellfun(@strtrim,lines,'UniformOutput',0);

% if(~isempty(ban_file) && all(cellfun(@(tmp)~isempty(tmp), ban_file)))% && (~isempty(ban_file{1})) )
if(~isempty(cell2str(ban_file)) && (~isempty(cell2str(ban_file))) )
    banned_images = filter_empty_strings(strsplit(fileread(cell2str(ban_file)),'\n'));
    cleaned_lines_banfree = setdiff(clean_lines,banned_images);
else
    cleaned_lines_banfree = clean_lines;
end

if(~isempty(ban_list))
    cleaned_lines_banfree = multifilter_string_list(cleaned_lines_banfree,ban_list,1);
end


image_generator = ImageGenerator(cleaned_lines_banfree);
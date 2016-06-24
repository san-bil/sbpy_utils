function generator = get_multipie_grouped_image_generator(varargin)
    
root_folder = '/vol/hci2/Databases/video/MultiPIE';

if(~exist(root_folder,'dir')==7)
    error('    You need to mount the multipie database at /vol/hci2/Databases/video/MultiPIE   ')
end
all_matchers = {};

for i = 1:length(varargin)
    matcher = get_multipie_file_path(varargin{i});
    all_matchers{i} = matcher;
end

generator = get_grouped_image_generator(root_folder,all_matchers,@get_multipie_subject_session_expr,1,cellcell([length(all_matchers) 1],1,''),{});

